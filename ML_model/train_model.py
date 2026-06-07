import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, roc_curve
import warnings

warnings.filterwarnings('ignore')

# 1. Load Data
df = pd.read_csv('zomato_cleaned.csv.gz', encoding='latin-1')

# Target Variable
median_votes = df['votes'].median()
df['success'] = (df['votes'] > median_votes).astype(int)

class_balance = df['success'].value_counts(normalize=True)
print("Class Balance:")
print(class_balance)

# Drop forbidden columns
cols_to_drop = ['votes', 'rate', 'url', 'address', 'phone', 'reviews_list']
df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

# Feature Engineering
if 'online_order' in df.columns:
    df['online_order'] = df['online_order'].map({'Yes': 1, 'No': 0}).fillna(0)

if 'book_table' in df.columns:
    df['book_table'] = df['book_table'].map({'Yes': 1, 'No': 0}).fillna(0)

cost_col = 'approx_cost(for two people)'
if cost_col not in df.columns and 'approx_cost' in df.columns:
    cost_col = 'approx_cost'

if cost_col in df.columns:
    if df[cost_col].dtype == object:
        df[cost_col] = df[cost_col].astype(str).str.replace(',', '').astype(float)
    df[cost_col] = df[cost_col].fillna(df[cost_col].median())

if 'rest_type' in df.columns:
    df = pd.get_dummies(df, columns=['rest_type'], drop_first=True, dtype=int)

type_col = 'listed_in(type)'
if type_col in df.columns:
    df = pd.get_dummies(df, columns=[type_col], drop_first=True, dtype=int)

if 'listed_in(city)' in df.columns:
    df = df.drop(columns=['listed_in(city)'])
if 'name' in df.columns:
    df = df.drop(columns=['name'])

if 'location' in df.columns:
    location_target_mean = df.groupby('location')['success'].mean()
    df['location'] = df['location'].map(location_target_mean)
    df['location'] = df['location'].fillna(df['success'].mean())

if 'cuisines' in df.columns:
    df['cuisines'] = df['cuisines'].astype(str)
    all_cuisines = df['cuisines'].str.split(', ').explode()
    top_10_cuisines = all_cuisines.value_counts().head(10).index.tolist()
    
    for cuisine in top_10_cuisines:
        df[f'cuisine_{cuisine}'] = df['cuisines'].apply(lambda x: 1 if cuisine in str(x).split(', ') else 0)
        
    df = df.drop(columns=['cuisines'])

for col in df.select_dtypes(include=['object']).columns:
    df = df.drop(columns=[col])

df = df.fillna(0)

# Train/Test Split
X = df.drop(columns=['success'])
y = df['success']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

use_balanced = class_balance.max() > 0.60
cw = 'balanced' if use_balanced else None

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, class_weight=cw, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_leaf=5, class_weight=cw, random_state=42, n_jobs=-1),
    'XGBoost': XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1, eval_metric='logloss', random_state=42)
}

scaler = StandardScaler()
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()
X_train_scaled[X_train.columns] = scaler.fit_transform(X_train)
X_test_scaled[X_train.columns] = scaler.transform(X_test)

results = []
fig_roc, ax_roc = plt.subplots(figsize=(8, 6))
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for name, model in models.items():
    X_tr = X_train_scaled if name == 'Logistic Regression' else X_train
    X_te = X_test_scaled if name == 'Logistic Regression' else X_test
        
    model.fit(X_tr, y_train)
    y_pred = model.predict(X_te)
    y_prob = model.predict_proba(X_te)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    prec = report['weighted avg']['precision']
    rec = report['weighted avg']['recall']
    f1 = report['weighted avg']['f1-score']
    roc_auc = roc_auc_score(y_test, y_prob)
    
    cv_scores = cross_val_score(model, X_tr, y_train, cv=skf, scoring='f1')
    
    results.append({
        'Model': name,
        'Accuracy': f"{acc:.4f}",
        'Precision': f"{prec:.4f}",
        'Recall': f"{rec:.4f}",
        'F1': f"{f1:.4f}",
        'ROC-AUC': f"{roc_auc:.4f}",
        'CV F1': f"{cv_scores.mean():.4f}±{cv_scores.std():.4f}"
    })
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5,4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix: {name}')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    plt.savefig(f'cm_{name.replace(" ", "_")}.png')
    plt.close()
    
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    ax_roc.plot(fpr, tpr, label=f'{name} (AUC = {roc_auc:.4f})')
    
    if name == 'Random Forest':
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:20]
        plt.figure(figsize=(10, 8))
        plt.title("Top 20 Feature Importances (Random Forest)")
        plt.barh(range(20), importances[indices][::-1], align="center")
        plt.yticks(range(20), [X_train.columns[i] for i in indices][::-1])
        plt.xlabel("Relative Importance")
        plt.tight_layout()
        plt.savefig('rf_feature_importances.png')
        plt.close()
        top_3_features = [X_train.columns[i] for i in indices[:3]]

ax_roc.plot([0, 1], [0, 1], 'k--')
ax_roc.set_xlabel('False Positive Rate')
ax_roc.set_ylabel('True Positive Rate')
ax_roc.set_title('ROC Curve Comparison')
ax_roc.legend(loc='lower right')
fig_roc.tight_layout()
fig_roc.savefig('roc_curve_comparison.png')
plt.close(fig_roc)

print("\n| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | CV F1 (mean±std) |")
print("|---|---|---|---|---|---|---|")
for r in results:
    print(f"| {r['Model']} | {r['Accuracy']} | {r['Precision']} | {r['Recall']} | {r['F1']} | {r['ROC-AUC']} | {r['CV F1']} |")
print("\nTop 3 features:", top_3_features)
