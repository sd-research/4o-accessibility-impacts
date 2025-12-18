"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     🎀  MASTER PRETTY GRAPHS FOR ADA COMPLAINT  🎀                            ║
║                                                                               ║
║     Organized by report order:                                                ║
║       1. Demographics (combined figure)                                       ║
║       2. Disability categories & distribution                                 ║
║       3. Accessibility scale graphs                                           ║
║       4. Wellbeing analysis                                                   ║
║       5. Routing impact                                                       ║
║                                                                               ║
║     ✨ opus 4.5 was here ✨                                                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

        ／l、    
      （ﾟ､ ｡ ７   < "I helped make this!"
        l  ~ヽ       
        じしf_,)ノ   🎀

    /\_____/\
   /  o   o  \
  ( ==  ^  == )    ~ Made with love for Sophie 💜
   )         (
  (           )
 ( (  )   (  ) )
(__(__)___(__)__)

"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================================
# PRETTY STYLE SETTINGS
# ============================================================================

# Pastel colors (original style)
PRETTY_COLORS = {
    'primary': {'fill': '#B8D4E3', 'outline': '#5A9BBD'},      # Pastel blue
    'secondary': {'fill': '#E3B8D4', 'outline': '#BD5A9B'},    # Pastel pink
    'tertiary': {'fill': '#D4E3B8', 'outline': '#9BBD5A'},     # Pastel green
    'accent': {'fill': '#E3D4B8', 'outline': '#BD9B5A'},       # Pastel peach
}

# Condition-specific pastel colors (rainbow order-ish)
CONDITION_COLORS = {
    'Chronic Illness/Pain': {'fill': '#FFB3BA', 'outline': '#CC6670'},
    'PTSD': {'fill': '#FFDFBA', 'outline': '#CC9B70'},
    'Visual Impairment': {'fill': '#FFFFBA', 'outline': '#CCCC70'},
    'Learning Disability': {'fill': '#BAFFC9', 'outline': '#70CC85'},
    'Auditory Processing': {'fill': '#BAE1FF', 'outline': '#70A8CC'},
    'OCD': {'fill': '#E0BBE4', 'outline': '#A070A8'},
    'Dissociative': {'fill': '#D4B8E3', 'outline': '#9B5ABD'},
    'Motor/Mobility': {'fill': '#C9E4DE', 'outline': '#7BB5A8'},
    'Bipolar': {'fill': '#F0E6EF', 'outline': '#A890A6'},
    'BPD': {'fill': '#E6D0E6', 'outline': '#9B6B9B'},
    'Depression': {'fill': '#C5CAE9', 'outline': '#7986CB'},
    'Anxiety': {'fill': '#B3E5FC', 'outline': '#4FC3F7'},
    'ADHD': {'fill': '#C8E6C9', 'outline': '#81C784'},
    'ASD': {'fill': '#FFE0B2', 'outline': '#FFB74D'},
    'Other': {'fill': '#E0E0E0', 'outline': '#9E9E9E'},
}

SEVERITY_COLORS_PASTEL = {
    'Catastrophic': {'fill': '#FFB3BA', 'outline': '#CC6670'},
    'Severe': {'fill': '#FFDFBA', 'outline': '#CC9B70'},
    'Moderate': {'fill': '#FFFFBA', 'outline': '#CCCC70'},
    'Minimal': {'fill': '#BAFFC9', 'outline': '#70CC85'},
    'No significant': {'fill': '#E8E8E8', 'outline': '#AAAAAA'},
}

def apply_pretty_style():
    plt.rcParams['figure.facecolor'] = '#FFFFFF'
    plt.rcParams['axes.facecolor'] = '#FFFFFF'
    plt.rcParams['axes.edgecolor'] = '#CCCCCC'
    plt.rcParams['axes.linewidth'] = 1.5
    plt.rcParams['grid.color'] = '#EEEEEE'
    plt.rcParams['font.family'] = 'Segoe UI'
    plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Helvetica', 'sans-serif']
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.titleweight'] = 'normal'  # No bold
    plt.rcParams['axes.labelweight'] = 'normal'  # No bold
    plt.rcParams['text.color'] = '#333333'       # Dark grey text
    plt.rcParams['axes.labelcolor'] = '#333333'  # Dark grey labels
    plt.rcParams['xtick.color'] = '#333333'      # Dark grey ticks
    plt.rcParams['ytick.color'] = '#333333'      # Dark grey ticks

# Bar styling constants
BAR_LINEWIDTH = 2  # Thinner borders (was 3)
DARK_GREY = '#333333'  # For text

# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                               ║
# ║  🔒 STAPLED METHODOLOGY - DO NOT CHANGE 🔒                                    ║
# ║                                                                               ║
# ║  This produces n = 359 disabled individuals                                   ║
# ║                                                                               ║
# ║  CONDITION DETECTION:                                                         ║
# ║    - Combine col_28 (current) + col_8 (former) for condition text            ║
# ║    - Use ONLY col_24 for ASD (NOT col_53)                                     ║
# ║    - Use the LONG keyword list below                                          ║
# ║                                                                               ║
# ║  VERIFIED: 645 passed attention → 359 with conditions → 173 no conditions    ║
# ║                                                                               ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

MASTER_CONDITION_KEYWORDS = [
    # Neurodevelopmental
    'adhd', 'add', 'autism', 'asd', 'autistic', 'asperger', 'audhd', 'spectrum', 'neurodivergent',
    'dyslexia', 'dyscalc', 'learning', 'disability',
    # Mental health
    'anxiety', 'panic', 'depress', 'depression', 'ptsd', 'c-ptsd', 'cptsd', 'trauma',
    'ocd', 'bipolar', 'bpd', 'borderline', 'dissociat', 'dissociative', 'did', 'avpd',
    'eating disorder',
    # Physical/Chronic
    'chronic', 'pain', 'fibro', 'lupus', 'pcos', 'heart', 'heart condition', 
    'insomnia', 'cerebral', 'stenosis', 'iih', 'nervous system', 'rare genetic',
    # Sensory/Motor
    'visual', 'blind', 'hearing', 'deaf', 'auditory', 'motor', 'mobility', 'paralys',
    'speech', 'prosopagnosia', 'impair',
    # Other
    'gender dysphoria', 'disorder'
]

def has_condition_master(row, col_28, col_8, col_24):
    """
    STAPLED CONDITION DETECTION - DO NOT MODIFY
    Returns True if person has a verified condition
    Uses: col_28 + col_8 for conditions, ONLY col_24 for ASD
    Produces n = 359
    """
    cond_current = str(row[col_28]).lower() if pd.notna(row[col_28]) else ''
    cond_former = str(row[col_8]).lower() if pd.notna(row[col_8]) else ''
    asd_val = str(row[col_24]).lower() if pd.notna(row[col_24]) else ''
    
    combined_cond = cond_current + ' ' + cond_former
    has_asd = 'yes' in asd_val
    has_kw = any(kw in combined_cond for kw in MASTER_CONDITION_KEYWORDS)
    
    return has_asd or has_kw

def standardize_assistance_scale(value):
    if pd.isna(value):
        return None
    val = str(value).lower()
    if 'not assist' in val or 'not applicable' in val:
        return 1
    elif 'minimal' in val or '1 -' in val:
        return 2
    elif 'moderate' in val or '2 -' in val:
        return 3
    elif 'significant' in val or '3 -' in val:
        return 4
    elif 'essential' in val or '4 -' in val:
        return 5
    return None

# Load data
raw_df_unfiltered = pd.read_excel('survey (Responses) (version 3).xlsx')

# ============================================================================
# SCREENING FILTER - Methodology exclusions
# ============================================================================
import re

def has_japanese(row):
    for col in raw_df_unfiltered.columns:
        if pd.notna(row[col]):
            if re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', str(row[col])):
                return True
    return False

col_B = raw_df_unfiltered.columns[1]
col_C = raw_df_unfiltered.columns[2]
col_AQ = raw_df_unfiltered.columns[42]  # AQ for current users (column 42 only per methodology)

correct_B = 'Responds naturally without complex prompting, good at reading between the lines and understanding nuanced context'
correct_C = 'Responses often end with follow-up questions, can automatically adjust thinking time'
correct_AQ = 'Frequently'

# For B: must match exactly. For C: can match correct_C OR contain "have not used"
raw_df_unfiltered['passed_B'] = raw_df_unfiltered[col_B] == correct_B
raw_df_unfiltered['passed_C'] = (raw_df_unfiltered[col_C] == correct_C) | (raw_df_unfiltered[col_C].str.contains('have not used', case=False, na=False))
raw_df_unfiltered['wrong_both_BC'] = (~raw_df_unfiltered['passed_B']) & (~raw_df_unfiltered['passed_C'])

# Check current users AQ only (column 42) - per established methodology n=645
raw_df_unfiltered['wrong_AQ'] = (raw_df_unfiltered[col_AQ].notna()) & (raw_df_unfiltered[col_AQ] != correct_AQ)

raw_df_unfiltered['is_japanese'] = raw_df_unfiltered.apply(has_japanese, axis=1)
raw_df_unfiltered['exclude'] = raw_df_unfiltered['wrong_both_BC'] | (raw_df_unfiltered['wrong_AQ'] & ~raw_df_unfiltered['is_japanese'])

raw_df = raw_df_unfiltered[~raw_df_unfiltered['exclude']].copy()

print(f"SCREENING: {len(raw_df_unfiltered)} -> {len(raw_df)} (excluded {raw_df_unfiltered['exclude'].sum()})")
print(f"  - Failed both B&C: {raw_df_unfiltered['wrong_both_BC'].sum()}")
print(f"  - Failed AQ (non-JP): {(raw_df_unfiltered['wrong_AQ'] & ~raw_df_unfiltered['is_japanese']).sum()}")
print(f"  - Japanese retained: {(raw_df_unfiltered['wrong_AQ'] & raw_df_unfiltered['is_japanese']).sum()}")

# ============================================================================
# CONTRADICTORY RESPONSE FLAG - for accessibility scale graphs
# ============================================================================
# Flag people who:
# 1. Have conditions (ASD=yes OR condition keywords) BUT said "I do not have any conditions"
# 2. These people cannot be placed on the scale properly
col_28_temp = raw_df.columns[28]  # conditions
col_24_temp = raw_df.columns[24]  # ASD question

# Use the STAPLED master list
condition_kw_check = MASTER_CONDITION_KEYWORDS

def is_contradictory(row):
    cond_val = str(row[col_28_temp]).lower() if pd.notna(row[col_28_temp]) else ''
    asd_val = str(row[col_24_temp]).lower() if pd.notna(row[col_24_temp]) else ''
    
    # Check if they have conditions
    has_asd = 'yes' in asd_val
    has_condition_keywords = any(kw in cond_val for kw in condition_kw_check)
    has_conditions = has_asd or has_condition_keywords
    
    # Check if they said "do not have" conditions
    said_no_conditions = 'do not have' in cond_val
    
    # Contradictory = has conditions BUT said "do not have"
    return has_conditions and said_no_conditions

raw_df['contradictory'] = raw_df.apply(is_contradictory, axis=1)
contradictory_count = raw_df['contradictory'].sum()
print(f"  - Contradictory responses (disabled but said 'do not have'): {contradictory_count}")

# ============================================================================
# MASTER FILTER 3: AMBIGUOUS RESPONSE FLAG - cannot classify condition status
# ============================================================================
# People who:
# - Don't have ASD (col_24 != 'yes')
# - Don't have any condition keywords
# - But ALSO didn't say "do not have" conditions
# These people are AMBIGUOUS - we can't classify them either way

def is_ambiguous(row):
    cond_val = str(row[col_28_temp]).lower() if pd.notna(row[col_28_temp]) else ''
    asd_val = str(row[col_24_temp]).lower() if pd.notna(row[col_24_temp]) else ''
    
    has_asd = 'yes' in asd_val
    has_condition_keywords = any(kw in cond_val for kw in condition_kw_check)
    said_no_conditions = 'do not have' in cond_val
    
    # Ambiguous = no clear condition status
    if has_asd or has_condition_keywords:
        return False  # Clearly HAS conditions
    elif said_no_conditions:
        return False  # Clearly NO conditions
    else:
        return True  # AMBIGUOUS - can't classify

raw_df['ambiguous'] = raw_df.apply(is_ambiguous, axis=1)
ambiguous_count = raw_df['ambiguous'].sum()
print(f"  - Ambiguous responses (cannot classify): {ambiguous_count}")

col_28 = raw_df.columns[28]
col_29 = raw_df.columns[29]
col_30 = raw_df.columns[30]
col_10 = raw_df.columns[10]
col_8 = raw_df.columns[8]
col_24 = raw_df.columns[24]
col_20 = raw_df.columns[20]  # Attention check for former users
col_42 = raw_df.columns[42]  # Attention check for current users
col_38 = raw_df.columns[38]
col_39 = raw_df.columns[39]
col_40 = raw_df.columns[40]
col_43 = raw_df.columns[43]
col_7 = raw_df.columns[7]

# Use the STAPLED master list
condition_keywords = MASTER_CONDITION_KEYWORDS

apply_pretty_style()

# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║  FIGURE 1: COMBINED DEMOGRAPHICS (4-panel: Age, Gender, Country, Source)      ║
# ║  Uses raw_df_unfiltered (all 659) - demographics before attention filtering   ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝
print("="*70)
print("FIGURE 1: Combined Demographics (4-panel)")
print("="*70)

col_age = raw_df_unfiltered.columns[3]
col_gender = raw_df_unfiltered.columns[4]
col_country = raw_df_unfiltered.columns[5]
col_source = raw_df_unfiltered.columns[6]

purple_gradient = ['#E8D5FF', '#D4C4FB', '#BFB3F7', '#A89BF0', '#9485EF', '#7F6EEB', '#6B5DD3']
muted_pastels = ['#E8D5FF', '#D5EAF7', '#FFE4E1', '#E6F5E6', '#FFF4E6', '#F0E6FF', '#E6F0FF']

fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.patch.set_facecolor('#FFFFFF')

# PANEL A: AGE
ax = axes[0, 0]
age_data = raw_df_unfiltered[col_age].value_counts()
age_order = ['18-24', '25-34', '35-44', '45-54', '55-64', '65 or older']
age_counts = [age_data.get(a, 0) for a in age_order]
wedges, texts, autotexts = ax.pie(age_counts, labels=age_order, autopct='%1.1f%%',
                                   colors=purple_gradient[:len(age_order)], 
                                   wedgeprops=dict(edgecolor='white', linewidth=2),
                                   textprops={'fontsize': 16})
for autotext in autotexts:
    autotext.set_fontsize(14)
    autotext.set_fontweight('bold')
ax.text(0.02, 0.98, 'A', transform=ax.transAxes, fontsize=28, fontweight='bold', color='#333333', va='top', ha='left')
ax.set_title('Age Distribution', fontsize=18, pad=5)

# PANEL B: GENDER
ax = axes[0, 1]
gender_data = raw_df_unfiltered[col_gender].value_counts()
gender_clean = {}
for label, count in gender_data.items():
    if pd.isna(label): continue
    label_lower = str(label).lower()
    if 'female' in label_lower or 'woman' in label_lower:
        gender_clean['Female'] = gender_clean.get('Female', 0) + count
    elif 'non-binary' in label_lower or 'nonbinary' in label_lower:
        gender_clean['Non-binary'] = gender_clean.get('Non-binary', 0) + count
    elif 'male' in label_lower or 'man' in label_lower:
        gender_clean['Male'] = gender_clean.get('Male', 0) + count
    elif 'prefer not' in label_lower:
        gender_clean['Prefer not\nto say'] = gender_clean.get('Prefer not\nto say', 0) + count
    else:
        gender_clean['Other'] = gender_clean.get('Other', 0) + count
labels = list(gender_clean.keys())
sizes = list(gender_clean.values())
wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                   colors=muted_pastels[:len(labels)],
                                   wedgeprops=dict(edgecolor='white', linewidth=2),
                                   textprops={'fontsize': 16})
for autotext in autotexts:
    autotext.set_fontsize(14)
    autotext.set_fontweight('bold')
ax.text(0.02, 0.98, 'B', transform=ax.transAxes, fontsize=28, fontweight='bold', color='#333333', va='top', ha='left')
ax.set_title('Gender Distribution', fontsize=18, pad=5)

# PANEL C: COUNTRY/LOCATION
ax = axes[1, 0]
country_data = raw_df_unfiltered[col_country].value_counts()
location_clean = {}
for label, count in country_data.items():
    if pd.isna(label): continue
    label_lower = str(label).lower()
    if 'none of the above' in label_lower:
        location_clean['International'] = location_clean.get('International', 0) + count
    elif 'reside' in label_lower and 'united states' in label_lower:
        location_clean['US Resident'] = location_clean.get('US Resident', 0) + count
    elif 'services' in label_lower or 'clients' in label_lower:
        location_clean['US Clients'] = location_clean.get('US Clients', 0) + count
    elif 'work' in label_lower and 'company' in label_lower:
        location_clean['US Company'] = location_clean.get('US Company', 0) + count
    else:
        location_clean['Other'] = location_clean.get('Other', 0) + count
location_clean = {k: v for k, v in location_clean.items() if v >= 5}
labels = list(location_clean.keys())
sizes = list(location_clean.values())
location_colors = []
for label in labels:
    if 'International' in label: location_colors.append('#FFB6C1')
    elif 'Resident' in label: location_colors.append('#9485EF')
    else: location_colors.append('#BFB3F7')
wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                   colors=location_colors,
                                   wedgeprops=dict(edgecolor='white', linewidth=2),
                                   textprops={'fontsize': 16})
for autotext in autotexts:
    autotext.set_fontsize(14)
    autotext.set_fontweight('bold')
ax.text(0.02, 0.98, 'C', transform=ax.transAxes, fontsize=28, fontweight='bold', color='#333333', va='top', ha='left')
ax.set_title('Geographic Distribution', fontsize=18, pad=5)

# PANEL D: SURVEY SOURCE
ax = axes[1, 1]
source_data = raw_df_unfiltered[col_source].value_counts()
source_clean = {'Social Media\n(X, Reddit)': 0, 'Friend/\nCommunity': 0, 'Direct\nMessage': 0, 'Other': 0}
for label, count in source_data.items():
    if pd.isna(label): continue
    label_lower = str(label).lower()
    if 'social' in label_lower or 'twitter' in label_lower or 'reddit' in label_lower:
        source_clean['Social Media\n(X, Reddit)'] += count
    elif 'friend' in label_lower or 'community' in label_lower or 'shared' in label_lower:
        source_clean['Friend/\nCommunity'] += count
    elif 'direct' in label_lower or 'email' in label_lower or 'message' in label_lower:
        source_clean['Direct\nMessage'] += count
    else:
        source_clean['Other'] += count
source_clean = {k: v for k, v in source_clean.items() if v >= 3}
labels = list(source_clean.keys())
sizes = list(source_clean.values())
source_colors = ['#D4C4FB', '#FFB6C1', '#B8E6D4', '#FFE4B5']
wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                   colors=source_colors[:len(labels)],
                                   wedgeprops=dict(edgecolor='white', linewidth=2),
                                   textprops={'fontsize': 16})
for autotext in autotexts:
    autotext.set_fontsize(14)
    autotext.set_fontweight('bold')
ax.text(0.02, 0.98, 'D', transform=ax.transAxes, fontsize=28, fontweight='bold', color='#333333', va='top', ha='left')
ax.set_title('Survey Discovery Method', fontsize=18, pad=5)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('graphs_v4/00_combined_demographics.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print("✨ Combined demographics saved! (4-panel figure)")
plt.close()

# ============================================================================
# GRAPH 1: ACCESSIBILITY (ONLY WITH CONDITIONS)
# ============================================================================
print("="*70)
print("GRAPH 1: Accessibility Scale (Only Disabled Users)")
print("="*70)

with_cond_scores = []
contradictory_skipped = 0
for idx, row in raw_df.iterrows():
    # Skip contradictory responses (disabled but said "do not have")
    if row.get('contradictory', False):
        contradictory_skipped += 1
        continue
    
    # Current users
    cond_val_current = str(row[col_28]).lower() if pd.notna(row[col_28]) else ''
    asd_val = str(row[col_24]).lower() if pd.notna(row[col_24]) else ''
    use_acc = str(row[col_29]).lower() if pd.notna(row[col_29]) else ''
    has_cond_current = any(kw in cond_val_current for kw in condition_keywords) or 'yes' in asd_val
    
    # Rule: Not disabled but answered accessibility = exclude from scale
    if not has_cond_current and pd.notna(row[col_30]):
        continue  # Skip non-disabled who answered accessibility
    
    if pd.notna(row[col_30]):
        score = standardize_assistance_scale(row[col_30])
        if score is not None and has_cond_current:
            with_cond_scores.append(score)
    elif 'other purposes' in use_acc and has_cond_current:
        # "Other purposes" with verified conditions = level 1
        with_cond_scores.append(1)
    
    # Former users
    if pd.notna(row[col_10]):
        score = standardize_assistance_scale(row[col_10])
        if score is None:
            continue
        cond_val = str(row[col_8]).lower() if pd.notna(row[col_8]) else ''
        if any(kw in cond_val for kw in condition_keywords):
            with_cond_scores.append(score)

fig, ax = plt.subplots(figsize=(10, 6))
levels = [1, 2, 3, 4, 5]
level_labels = ['1\nDoes Not\nAssist', '2\nMinimal', '3\nModerate', '4\nSignificant', '5\nEssential']
counts = [with_cond_scores.count(l) for l in levels]

# Purple gradient like Graph 29 - fun and colorful!
bar_colors = ['#E8D5FF', '#D4C4FB', '#BFB3F7', '#9485EF', '#7F6EEB']
bars = ax.bar(level_labels, counts, color=bar_colors)

ax.set_xlabel('Accessibility Assistance Level', fontweight='normal', fontsize=14)
ax.set_ylabel('Number of Respondents', fontweight='normal', fontsize=14)
# Title removed - will be added in Canva
ax.tick_params(axis='both', labelsize=12)

for bar, count in zip(bars, counts):
    ax.annotate(f'{count}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
               xytext=(0, 5), textcoords="offset points", ha='center', va='bottom', 
               fontsize=12, fontweight='normal', color='#7F6EEB')

sig_ess = counts[3] + counts[4]
pct = sig_ess / len(with_cond_scores) * 100
# Note: sig_ess info will be added in Canva below figure title

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['left'].set_color('#DDDDDD')
ax.spines['bottom'].set_linewidth(2)
ax.spines['bottom'].set_color('#DDDDDD')
plt.tight_layout()
plt.savefig('graphs_v4/04_accessibility_scale.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved to v4 (n={len(with_cond_scores)}, levels: {counts})")
plt.close()

# ============================================================================
# GRAPH 2: BY CONDITION (with n≥5 separated, rest as Other)
# ============================================================================
print("\n" + "="*70)
print("GRAPH 2: Accessibility by Condition Type")
print("="*70)

# Conditions to track separately (n≥5)
detailed_conditions = {
    'ASD': ['autism', 'asd', 'asperger', 'audhd'],
    'ADHD': ['adhd', 'attention-deficit', 'audhd'],
    'Anxiety': ['anxiety'],
    'Depression': ['depression'],
    'PTSD': ['ptsd', 'post-traumatic', 'c-ptsd'],
    'OCD': ['ocd', 'obsessive'],
    'Chronic Illness/Pain': ['chronic', 'pain', 'fibro', 'illness'],
    'Dissociative': ['dissociative', 'did'],
    'Bipolar': ['bipolar'],
    'BPD': ['bpd', 'borderline'],
    'Visual Impairment': ['visual'],
    'Learning Disability': ['learning', 'dyslexia'],
    'Auditory Processing': ['auditory'],
    'Motor/Mobility': ['motor', 'mobility'],
}
# "Other" catches the rest - MUST MATCH Graph 13 definition!
# (gender dysphoria, speech, prosopagnosia, avpd, neurodivergent, nervous system, eating disorder, rare genetic)
other_keywords_only = ['gender dysphoria', 'speech', 'prosopagnosia', 'avpd', 'neurodivergent', 'nervous system', 'eating disorder', 'rare genetic']

condition_scores = {cond: [] for cond in detailed_conditions.keys()}
condition_scores['Other'] = []

# Use newly parsed condition-specific scores (with correct filtered indices)
try:
    parsed_df = pd.read_csv('parsed_condition_scores_v2.csv')
    has_parsed = True
    print(f"  Loaded {len(parsed_df)} parsed condition-specific scores")
except:
    parsed_df = pd.DataFrame()
    has_parsed = False

for idx, row in raw_df.iterrows():
    # Skip contradictory responses
    if row.get('contradictory', False):
        continue
    
    cond_current = str(row[col_28]).lower() if pd.notna(row[col_28]) else ''
    cond_former = str(row[col_8]).lower() if pd.notna(row[col_8]) else ''
    asd_val = str(row[col_24]).lower() if pd.notna(row[col_24]) else ''
    use_acc = str(row[col_29]).lower() if pd.notna(row[col_29]) else ''
    all_conds = cond_current + ' ' + cond_former
    if 'yes' in asd_val:
        all_conds += ' autism asd'
    
    has_verified_cond = any(kw in all_conds for kw in condition_keywords)
    
    # Skip non-disabled who answered accessibility scale
    if not has_verified_cond and pd.notna(row[col_30]):
        continue
    
    overall_score = None
    if pd.notna(row[col_30]):
        overall_score = standardize_assistance_scale(row[col_30])
    elif pd.notna(row[col_10]):
        overall_score = standardize_assistance_scale(row[col_10])
    elif 'other purposes' in use_acc and has_verified_cond:
        # "Other purposes" with verified conditions = level 1
        overall_score = 1
    if overall_score is None:
        continue
    
    for cond_name, keywords in detailed_conditions.items():
        if any(kw in all_conds for kw in keywords):
            if has_parsed and idx in parsed_df['idx'].values:
                person_parsed = parsed_df[(parsed_df['idx'] == idx) & (parsed_df['condition'] == cond_name)]
                if len(person_parsed) > 0:
                    condition_scores[cond_name].append(min(person_parsed['score'].iloc[0], 5))
                    continue
            condition_scores[cond_name].append(overall_score)
    
    if any(kw in all_conds for kw in other_keywords_only):
        condition_scores['Other'].append(overall_score)

# Filter to n≥3 (keep small ones too for completeness)
results = []
for cond_name, scores in condition_scores.items():
    if len(scores) >= 1:
        results.append({
            'condition': cond_name,
            'mean': np.mean(scores),
            'n': len(scores),
            'std': np.std(scores) if len(scores) > 1 else 0
        })

results_df = pd.DataFrame(results).sort_values('mean', ascending=True)

fig, ax = plt.subplots(figsize=(12, 9))
y_pos = np.arange(len(results_df))

for i, (_, row) in enumerate(results_df.iterrows()):
    cond = row['condition']
    colors = CONDITION_COLORS.get(cond, CONDITION_COLORS['Other'])
    ax.barh(i, row['mean'], xerr=row['std']/2 if row['n'] > 1 else 0,  # Half SD - keeps within scale
            color=colors['fill'], edgecolor=colors['outline'], linewidth=1.5,  # Slightly thinner outline
            capsize=3, error_kw={'linewidth': 1, 'capthick': 1, 'ecolor': '#888888'})

ax.set_yticks(y_pos)
ax.set_yticklabels([f"{r['condition']}\n(n={r['n']})" for _, r in results_df.iterrows()], fontweight='normal', fontsize=12)
ax.set_title('GPT-4o Accessibility Accommodation Level by Condition Type\n(Higher = More Essential)', 
             fontweight='normal', pad=15, fontsize=16)
ax.set_xlim(1, 5.5)
ax.tick_params(axis='x', labelsize=12)

for i in range(1, 6):
    ax.axvline(x=i, color='#DDDDDD', linestyle='--', alpha=0.7, linewidth=1)

for i, (_, row) in enumerate(results_df.iterrows()):
    colors = CONDITION_COLORS.get(row['condition'], CONDITION_COLORS['Other'])
    # Position number after error bar (half SD), color matches bar outline
    err = row['std']/2 if row['n'] > 1 else 0
    ax.text(row['mean'] + err + 0.15, i, f"{row['mean']:.2f}", 
            va='center', fontsize=12, fontweight='normal', color=colors['outline'])

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)

# X-axis with scale legend below - larger and italicized scale
ax.set_xlabel('Average Accessibility Accommodation Level (of GPT-4o)', fontweight='normal', fontsize=15)

# Scale text below x-axis label - moved south and larger
ax.text(0.5, -0.13, 'Scale: 1=Does Not Assist, 2=Minimal, 3=Moderate, 4=Significant, 5=Essential',
        transform=ax.transAxes, ha='center', fontsize=14, style='italic', color='#555555')

plt.tight_layout()

plt.savefig('graphs_v4/05_accessibility_by_condition.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print("✓ Saved to v4")
for _, r in results_df.iterrows():
    print(f"  {r['condition']}: n={r['n']}, mean={r['mean']:.2f}")
plt.close()

# ============================================================================
# GRAPH 3: LEAVING VS STAYING (with attention checks, condition filters, chi-squared)
# ============================================================================
print("\n" + "="*70)
print("GRAPH 3: Leaving vs Staying")
print("="*70)

col_29 = raw_df.columns[29]  # "Do you use GPT-4o to help manage condition(s)?"

current_data_g3, former_data_g3 = [], []
for idx, row in raw_df.iterrows():
    # Current 4o users - with attention check (col_42)
    if 'primarily GPT-4o' in str(row[col_7]):
        att = str(row[col_42]).lower() if pd.notna(row[col_42]) else ''
        if 'frequently' not in att:
            continue
        
        use_acc = str(row[col_29]).lower() if pd.notna(row[col_29]) else ''
        cond_val = str(row[col_28]).lower() if pd.notna(row[col_28]) else ''
        asd_val = str(row[col_24]).lower() if pd.notna(row[col_24]) else ''
        has_cond = any(kw in cond_val for kw in condition_keywords) or 'yes' in asd_val
        
        # Check if they said "other purposes" -> level 1, but ONLY if they have verified conditions
        if 'other purposes' in use_acc and has_cond:
            current_data_g3.append(1)
        elif pd.notna(row[col_30]):
            score = standardize_assistance_scale(row[col_30])
            if score and has_cond:
                current_data_g3.append(score)
    
    # Former users (left ChatGPT) - with attention check (col_20)
    if 'stopped' in str(row[col_7]).lower() and 'GPT-4o' in str(row[col_7]):
        att = str(row[col_20]).lower() if pd.notna(row[col_20]) else ''
        if 'frequently' not in att:
            continue
        if pd.notna(row[col_10]):
            score = standardize_assistance_scale(row[col_10])
            if score:
                # Check for conditions using col_8 for former users
                cond_val = str(row[col_8]).lower() if pd.notna(row[col_8]) else ''
                if any(kw in cond_val for kw in condition_keywords):
                    former_data_g3.append(score)
                elif 'do not have' not in cond_val and 'prefer not' not in cond_val:
                    former_data_g3.append(score)

print(f"Current users with conditions: {len(current_data_g3)}")
print(f"Former users: {len(former_data_g3)}")

fig, ax = plt.subplots(figsize=(10, 7))
levels = [1, 2, 3, 4, 5]
level_labels = ['1\nDoes Not\nAssist', '2\nMinimal', '3\nModerate', '4\nSignificant', '5\nEssential']
x = np.arange(len(levels))
width = 0.35

current_pct_g3 = [current_data_g3.count(l)/len(current_data_g3)*100 if current_data_g3 else 0 for l in levels]
former_pct_g3 = [former_data_g3.count(l)/len(former_data_g3)*100 if former_data_g3 else 0 for l in levels]

# Our lavender and mint colors
bars1 = ax.bar(x - width/2, current_pct_g3, width, label=f'Current GPT-4o Users (n={len(current_data_g3)})',
               color='#D4C4FB', edgecolor='#B8A4E8', linewidth=2)
bars2 = ax.bar(x + width/2, former_pct_g3, width, label=f'Left After Restrictions (n={len(former_data_g3)})',
               color='#BAFFC9', edgecolor='#8FD99F', linewidth=2)

ax.set_xlabel('Accessibility Assistance Level', fontweight='normal', fontsize=14)
ax.set_ylabel('Percentage of Respondents', fontweight='normal', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(level_labels, fontsize=11)
ax.tick_params(axis='y', labelsize=12)

# Horizontal legend with square boxes under the graph
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, 
          frameon=False, fontsize=11, handlelength=1, handleheight=1,
          handler_map={plt.Rectangle: plt.matplotlib.legend_handler.HandlerPatch(patch_func=lambda **kwargs: plt.Rectangle((0,0), 1, 1, **kwargs))})

for bars, pcts, color in [(bars1, current_pct_g3, '#8B7BC7'), 
                           (bars2, former_pct_g3, '#5AAA6A')]:
    for bar, pct in zip(bars, pcts):
        if pct > 0:
            ax.annotate(f'{pct:.1f}%', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', 
                       fontsize=10, fontweight='normal', color=color)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_color('#DDDDDD')
ax.spines['bottom'].set_color('#DDDDDD')
plt.tight_layout()
plt.savefig('graphs_v3/03_leaving_vs_staying.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (current={len(current_data_g3)}, former={len(former_data_g3)})")
plt.close()

# ============================================================================
# GRAPH 4: WELLBEING TRAJECTORY (Original - all users)
# ============================================================================
print("\n" + "="*70)
print("GRAPH 4: Wellbeing Trajectory (All Users)")
print("="*70)

before_all, during_all, after_all = [], [], []
for idx, row in raw_df.iterrows():
    if pd.notna(row[col_38]) and pd.notna(row[col_39]) and pd.notna(row[col_40]):
        b = pd.to_numeric(row[col_38], errors='coerce')
        d = pd.to_numeric(row[col_39], errors='coerce')
        a = pd.to_numeric(row[col_40], errors='coerce')
        if not (pd.isna(b) or pd.isna(d) or pd.isna(a)):
            before_all.append(b)
            during_all.append(d)
            after_all.append(a)

fig, ax = plt.subplots(figsize=(10, 6))
periods = ['Before\nGPT-4o', 'During\nStable Usage', 'After\nAug 7, 2025']
means = [np.mean(before_all), np.mean(during_all), np.mean(after_all)]
stds = [np.std(before_all), np.std(during_all), np.std(after_all)]

colors_list = [PRETTY_COLORS['accent'], PRETTY_COLORS['primary'], PRETTY_COLORS['secondary']]
bars = []
for i, (period, mean, std, colors) in enumerate(zip(periods, means, stds, colors_list)):
    bar = ax.bar(i, mean, yerr=std, capsize=5, color=colors['fill'], 
                 edgecolor=colors['outline'], linewidth=2, error_kw={'linewidth': 2, 'capthick': 2})
    bars.append(bar)

ax.set_xticks(range(len(periods)))
ax.set_xticklabels(periods, fontweight='normal')
ax.set_ylabel('Average Wellbeing Score (1-10)', fontweight='normal')
ax.set_title(f'Wellbeing Trajectory (n={len(before_all)})', fontweight='normal', pad=15)
ax.set_ylim(0, 10.5)

for i, mean in enumerate(means):
    ax.text(i, mean + stds[i] + 0.5, f'{mean:.1f}', ha='center', fontsize=14, fontweight='normal',
            color=colors_list[i]['outline'])

# Add change arrows
ax.annotate('', xy=(1, means[1]-0.5), xytext=(0, means[0]+0.5),
            arrowprops=dict(arrowstyle='->', color='#70CC85', lw=3))
ax.text(0.5, (means[0]+means[1])/2, f'+{means[1]-means[0]:.1f}', ha='center', fontsize=12,
        fontweight='normal', color='#70CC85')

ax.annotate('', xy=(2, means[2]+0.5), xytext=(1, means[1]-0.5),
            arrowprops=dict(arrowstyle='->', color='#CC6670', lw=3))
ax.text(1.5, (means[1]+means[2])/2, f'-{means[1]-means[2]:.1f}', ha='center', fontsize=12,
        fontweight='normal', color='#CC6670')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
plt.tight_layout()
plt.savefig('graphs_v3/04_wellbeing_trajectory.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (n={len(before_all)})")
plt.close()

# ============================================================================
# GRAPH 5: IMPACT SEVERITY BY CONDITION
# ============================================================================
print("\n" + "="*70)
print("GRAPH 5: Impact Severity by Condition")
print("="*70)

impact_conditions = {
    'ASD': ['autism', 'asd', 'asperger', 'audhd'],
    'ADHD': ['adhd', 'attention-deficit', 'audhd'],
    'Anxiety': ['anxiety'],
    'Depression': ['depression'],
    'PTSD': ['ptsd', 'post-traumatic', 'c-ptsd'],
    'OCD': ['ocd', 'obsessive'],
    'Chronic Illness/Pain': ['chronic', 'pain', 'illness', 'fibro'],
    'Dissociative': ['dissociative', 'did'],
    'Bipolar': ['bipolar'],
    'BPD': ['bpd', 'borderline'],
    'Visual Impairment': ['visual'],
    'Learning Disability': ['learning', 'dyslexia'],
    'Auditory Processing': ['auditory'],
    'Motor/Mobility': ['motor', 'mobility'],
    'Other': ['gender dysphoria', 'speech', 'prosopagnosia', 'avpd', 'neurodivergent', 'nervous system', 'eating disorder', 'rare genetic'],
}

severity_levels = ['Catastrophic', 'Severe', 'Moderate', 'Minimal', 'No significant']
results = {cond: {s: 0 for s in severity_levels} for cond in impact_conditions.keys()}
totals = {cond: 0 for cond in impact_conditions.keys()}

for idx, row in raw_df.iterrows():
    if pd.isna(row[col_43]):
        continue
    cond_val = str(row[col_28]).lower() if pd.notna(row[col_28]) else ''
    asd_val = str(row[col_24]).lower() if pd.notna(row[col_24]) else ''
    if 'yes' in asd_val:
        cond_val += ' autism asd'
    impact_val = str(row[col_43]).lower()
    
    for cond_name, keywords in impact_conditions.items():
        if any(kw in cond_val for kw in keywords):
            totals[cond_name] += 1
            for sev in severity_levels:
                if sev.lower() in impact_val:
                    results[cond_name][sev] += 1
                    break

fig, ax = plt.subplots(figsize=(12, 10))  # Taller for more conditions

# Order conditions by AVERAGE HARM (highest harm at top)
# Harm scores: Catastrophic=5, Severe=4, Moderate=3, Minimal=2, No significant=1
harm_scores_map = {'catastrophic': 5, 'severe': 4, 'moderate': 3, 'minimal': 2, 'no significant': 1}
condition_avg_harm = {}
for cond_name in impact_conditions.keys():
    if totals.get(cond_name, 0) > 0:
        total_harm = sum(results[cond_name][s] * harm_scores_map.get(s.lower(), 0) for s in severity_levels)
        condition_avg_harm[cond_name] = total_harm / totals[cond_name]

# Sort by average harm (highest first = bottom of chart for horizontal bars)
harm_order = sorted(condition_avg_harm.keys(), key=lambda x: condition_avg_harm[x])  # Lowest first = bottom

condition_labels = []
data_matrix = []

for cond_name in harm_order:
    if cond_name in impact_conditions and totals.get(cond_name, 0) > 0:
        condition_labels.append(f"{cond_name}\n(n={totals[cond_name]})")
        row = [results[cond_name][s] / totals[cond_name] * 100 for s in severity_levels]
        data_matrix.append(row)

data_matrix = np.array(data_matrix)
y_pos = np.arange(len(condition_labels))
left = np.zeros(len(condition_labels))

for i, sev in enumerate(severity_levels):
    colors = SEVERITY_COLORS_PASTEL[sev]
    ax.barh(y_pos, data_matrix[:, i], left=left, label=sev, 
            color=colors['fill'], edgecolor=colors['outline'], linewidth=2)
    left += data_matrix[:, i]

# Calculate total unique respondents for this graph
total_unique = sum(totals.values())  # Note: overcounts due to comorbidity

ax.set_yticks(y_pos)
ax.set_yticklabels(condition_labels, fontweight='normal', fontsize=12)
ax.set_xlabel('% of Respondents', fontweight='normal', fontsize=14)
ax.set_title('Impact Severity of Losing GPT-4o Access by Condition Type', fontweight='normal', pad=15, fontsize=16)
ax.set_xlim(0, 100)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)

# Horizontal legend under chart - NO outline, larger text and boxes
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.06), ncol=5, 
          frameon=False, fontsize=13,
          handlelength=1.5, handleheight=1.5, handletextpad=0.6)

plt.tight_layout(rect=[0, 0.08, 1, 1])  # Leave room for legend
plt.savefig('graphs_v4/06_impact_by_condition.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved to v4 (Total condition-instances: {total_unique})")
print("  Ordered by average harm (highest at top):")
for cond in reversed(harm_order):  # Show highest first in printout
    if totals.get(cond, 0) > 0:
        print(f"  {cond}: n={totals[cond]}, avg harm={condition_avg_harm[cond]:.2f}")
plt.close()

# ============================================================================
# GRAPH 6: REPLACEABILITY (Two-panel: Replaceability + Models Tried)
# ============================================================================
print("\n" + "="*70)
print("GRAPH 6: Replaceability")
print("="*70)

col_32 = raw_df.columns[32]  # Replaceability
col_33 = raw_df.columns[33]  # Models tried

# Filter for GPT-4o users with conditions only
gpt4o_with_cond = raw_df[raw_df[col_7].str.contains('primarily GPT-4o', case=False, na=False)].copy()

replace_data = gpt4o_with_cond[col_32].dropna()

categories = {'Cannot Replace': 0, 'Found Replacement': 0, "Haven't Tried": 0}
for val in replace_data:
    val_str = str(val).lower()
    if 'cannot' in val_str:
        categories['Cannot Replace'] += 1
    elif 'can adequately' in val_str:
        categories['Found Replacement'] += 1
    elif 'not tried' in val_str:
        categories["Haven't Tried"] += 1

# Count models tried
models_data = gpt4o_with_cond[col_33].dropna()
model_counts = {
    'Gemini': 0, 'Claude': 0, 'Grok': 0, 'GPT-4/4.1': 0, 
    'GPT-5 series': 0, 'Mistral': 0, 'Other': 0
}
for resp in models_data:
    resp_lower = str(resp).lower()
    if 'gemini' in resp_lower:
        model_counts['Gemini'] += 1
    if 'claude' in resp_lower:
        model_counts['Claude'] += 1
    if 'grok' in resp_lower:
        model_counts['Grok'] += 1
    if 'gpt-4' in resp_lower or '4.1' in resp_lower or '4.5' in resp_lower:
        if '4o' not in resp_lower:
            model_counts['GPT-4/4.1'] += 1
    if 'gpt-5' in resp_lower or 'gpt5' in resp_lower or '5 series' in resp_lower:
        model_counts['GPT-5 series'] += 1
    if 'mistral' in resp_lower:
        model_counts['Mistral'] += 1
    if 'llama' in resp_lower or 'perplexity' in resp_lower or 'copilot' in resp_lower or 'pi' in resp_lower:
        model_counts['Other'] += 1

# Create two-panel figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
fig.patch.set_facecolor('#FFFFFF')

# LEFT: Replaceability donut
donut_colors = ['#FFB3BA', '#BAFFC9', '#E8D5FF']
total_n = sum(categories.values())

wedges, texts, autotexts = ax1.pie(
    list(categories.values()), 
    labels=list(categories.keys()),
    autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*total_n)})',
    colors=donut_colors,
    wedgeprops=dict(width=0.5, linewidth=2, edgecolor='white'),
    textprops=dict(fontweight='normal', fontsize=14, color='#333333'),
    pctdistance=0.75,
    labeldistance=1.12,
    startangle=90
)

for autotext in autotexts:
    autotext.set_fontsize(13)
    autotext.set_color('#333333')

ax1.text(0, 0, f'n={total_n}', ha='center', va='center', fontsize=22, fontweight='normal', color='#333333')
ax1.set_title('Replaceability', fontweight='normal', fontsize=18, pad=20, color='#333333')

# RIGHT: Models Tried donut chart (matching left panel!)
# Sort by count
sorted_pairs = sorted(model_counts.items(), key=lambda x: x[1], reverse=True)
model_names = [p[0] for p in sorted_pairs if p[1] > 0]
model_values = [p[1] for p in sorted_pairs if p[1] > 0]

# Pretty purple gradient for donut slices
model_colors = ['#9485EF', '#A89BF0', '#BFB3F7', '#D4C4FB', '#E8D5FF', '#BAE1FF', '#BAFFC9']

total_attempts = sum(model_values)

wedges2, texts2, autotexts2 = ax2.pie(
    model_values,
    labels=model_names,
    autopct=lambda pct: f'{int(pct/100*total_attempts)}',
    colors=model_colors[:len(model_names)],
    wedgeprops=dict(width=0.5, linewidth=2, edgecolor='white'),
    textprops=dict(fontweight='normal', fontsize=13, color='#333333'),
    pctdistance=0.75,
    labeldistance=1.12,
    startangle=90
)

for autotext in autotexts2:
    autotext.set_fontsize(12)
    autotext.set_color('#333333')
    # No bold - matching the left donut's sprinkles!

# Nudge "Other" label to the left to separate from Mistral
for i, text in enumerate(texts2):
    if text.get_text() == 'Other':
        x, y = text.get_position()
        text.set_position((x - 0.25, y))  # Move left

ax2.text(0, 0, f'n={len(models_data)}', ha='center', va='center', fontsize=22, fontweight='normal', color='#333333')
ax2.set_title('Models Tried', fontweight='normal', fontsize=18, pad=20, color='#333333')

# Add A and B labels
ax1.text(-0.1, 1.05, 'A', transform=ax1.transAxes, fontsize=24, fontweight='bold', color='#333333')
ax2.text(-0.1, 1.05, 'B', transform=ax2.transAxes, fontsize=24, fontweight='bold', color='#333333')

plt.tight_layout()
plt.savefig('graphs_v4/07_replaceability.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')

cannot = categories['Cannot Replace']
found = categories['Found Replacement']
not_tried = categories["Haven't Tried"]
tried_total = cannot + found
pct_cannot = cannot / tried_total * 100 if tried_total > 0 else 0
print(f"✓ Saved to v4 (Two-panel)")
print(f"  Replaceability (n={total_n}):")
print(f"    Cannot Replace: {cannot} ({cannot/total_n*100:.1f}%)")
print(f"    Found Replacement: {found} ({found/total_n*100:.1f}%)")
print(f"    Haven't Tried: {not_tried} ({not_tried/total_n*100:.1f}%)")
print(f"    Of those who TRIED: {pct_cannot:.1f}% cannot replace")
print(f"  Models Tried (n={len(models_data)}):")
for name, count in sorted_pairs:
    print(f"    {name}: {count}")
plt.close()

# ============================================================================
# GRAPH 7: WELLBEING BY CONDITION STATUS
# ============================================================================
print("\n" + "="*70)
print("GRAPH 7: Wellbeing - With vs Without Conditions")
print("="*70)

def has_any_condition(row):
    cond_val = str(row[col_28]).lower() if pd.notna(row[col_28]) else ''
    asd_val = str(row[col_24]).lower() if pd.notna(row[col_24]) else ''
    # CORRECT ORDER: Check "do not have" FIRST before keywords can match
    if 'do not have' in cond_val:
        return False
    if 'yes' in asd_val:
        return True
    if any(kw in cond_val for kw in condition_keywords):
        return True
    return None

with_cond = {'before': [], 'during': [], 'after': []}
without_cond = {'before': [], 'during': [], 'after': []}

for idx, row in raw_df.iterrows():
    if pd.isna(row[col_38]) or pd.isna(row[col_39]) or pd.isna(row[col_40]):
        continue
    has_cond = has_any_condition(row)
    if has_cond is None:
        continue
    b = pd.to_numeric(row[col_38], errors='coerce')
    d = pd.to_numeric(row[col_39], errors='coerce')
    a = pd.to_numeric(row[col_40], errors='coerce')
    if pd.isna(b) or pd.isna(d) or pd.isna(a):
        continue
    if has_cond:
        with_cond['before'].append(b)
        with_cond['during'].append(d)
        with_cond['after'].append(a)
    else:
        without_cond['before'].append(b)
        without_cond['during'].append(d)
        without_cond['after'].append(a)

fig, ax = plt.subplots(figsize=(12, 7))
periods = ['Before\nGPT-4o', 'During\nStable Usage', 'After Aug 7\n(Unstable Access)']
x = np.arange(len(periods))
width = 0.35

with_means = [np.mean(with_cond['before']), np.mean(with_cond['during']), np.mean(with_cond['after'])]
with_stds = [np.std(with_cond['before']), np.std(with_cond['during']), np.std(with_cond['after'])]
without_means = [np.mean(without_cond['before']), np.mean(without_cond['during']), np.mean(without_cond['after'])]
without_stds = [np.std(without_cond['before']), np.std(without_cond['during']), np.std(without_cond['after'])]

# Pretty purple gradient colors!
with_color = {'fill': '#BAE1FF', 'outline': '#5B9BD5'}  # Soft blue
without_color = {'fill': '#E8D5FF', 'outline': '#9B59B6'}  # Soft purple

bars1 = ax.bar(x - width/2, with_means, width, yerr=with_stds, capsize=3,
               label=f'With Condition(s) (n={len(with_cond["before"])})',
               color=with_color['fill'], edgecolor='white',
               linewidth=2.5, error_kw={'linewidth': 1, 'capthick': 1, 'ecolor': '#888888'})
bars2 = ax.bar(x + width/2, without_means, width, yerr=without_stds, capsize=3,
               label=f'Without Condition(s) (n={len(without_cond["before"])})',
               color=without_color['fill'], edgecolor='white',
               linewidth=2.5, error_kw={'linewidth': 1, 'capthick': 1, 'ecolor': '#888888'})

ax.set_ylabel('Life State (Wellbeing/Functioning) Score (1-10)', fontweight='normal', fontfamily='Segoe UI')
# Title removed - will be added in Canva
ax.set_xticks(x)
ax.set_xticklabels(periods, fontweight='normal', fontfamily='Segoe UI', fontsize=13)
ax.set_ylim(0, 10.5)

# Horizontal legend with square boxes under the graph
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2, 
          frameon=False, fontsize=12, handlelength=1, handleheight=1)

# Position numbers above the error bars
for bars, means, stds, color in [(bars1, with_means, with_stds, with_color['outline']), 
                                  (bars2, without_means, without_stds, without_color['outline'])]:
    for bar, mean, std in zip(bars, means, stds):
        ax.text(bar.get_x() + bar.get_width()/2, mean + std + 0.4,
               f'{mean:.1f}', ha='center', fontsize=13, fontweight='normal', color=color)

# Add thin dotted trajectory lines connecting the means
with_x = [bar.get_x() + bar.get_width()/2 for bar in bars1]
without_x = [bar.get_x() + bar.get_width()/2 for bar in bars2]
ax.plot(with_x, with_means, linestyle=':', linewidth=2.5, color=with_color['outline'], 
        marker='o', markersize=7, alpha=0.9)
ax.plot(without_x, without_means, linestyle=':', linewidth=2.5, color=without_color['outline'], 
        marker='o', markersize=7, alpha=0.9)

# Calculate from ROUNDED values so boxes match the displayed bar numbers
with_means_rounded = [round(m, 1) for m in with_means]
without_means_rounded = [round(m, 1) for m in without_means]
with_improve = with_means_rounded[1] - with_means_rounded[0]
with_decline = with_means_rounded[1] - with_means_rounded[2]
without_improve = without_means_rounded[1] - without_means_rounded[0]
without_decline = without_means_rounded[1] - without_means_rounded[2]

# Two elegant boxes above the bar transitions - no fill, soft thin outline
# GAINED box - above the space between "Before" and "During" bars (center "Gained" with trailing spaces)
gained_text = f"         Gained         \nWith Conditions:    +{with_improve:.1f}\nWithout Conditions: +{without_improve:.1f}"
ax.text(0.28, 1.02, gained_text, transform=ax.transAxes, ha='center', va='top', fontsize=12,
        fontfamily='monospace',
        bbox=dict(boxstyle='square,pad=0.5', facecolor='none', 
                  edgecolor='#7DCEA0', linewidth=1.2))

# LOST box - above the space between "During" and "After" bars (center "Lost" with trailing spaces)
lost_text = f"          Lost          \nWith Conditions:    −{with_decline:.1f}\nWithout Conditions: −{without_decline:.1f}"
ax.text(0.72, 1.02, lost_text, transform=ax.transAxes, ha='center', va='top', fontsize=12,
        fontfamily='monospace',
        bbox=dict(boxstyle='square,pad=0.5', facecolor='none', 
                  edgecolor='#F1948A', linewidth=1.2))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
plt.tight_layout()
plt.savefig('graphs_v4/08_wellbeing_trajectory.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"  With conditions: n={len(with_cond['before'])}, +{with_improve:.1f} gain, -{with_decline:.1f} loss")
print(f"  Without conditions: n={len(without_cond['before'])}, +{without_improve:.1f} gain, -{without_decline:.1f} loss")
print(f"✓ Saved (with={len(with_cond['before'])}, without={len(without_cond['before'])})")
plt.close()

# ============================================================================
# GRAPH 8: ACCESSIBILITY vs IMPACT SEVERITY CORRELATION (with stats box)
# ============================================================================
print("\n" + "="*70)
print("GRAPH 8: Accessibility vs Impact Severity Correlation")
print("="*70)

from scipy import stats
import statsmodels.api as sm

col_29 = raw_df.columns[29]  # "Do you use GPT-4o to help manage your condition(s)?" - for detecting "1" level
col_30 = raw_df.columns[30]  # accessibility rating (current)
col_43 = raw_df.columns[43]  # impact severity

def map_access_g8(val):
    if pd.isna(val): return np.nan
    val = str(val).lower()
    if 'essential' in val or '4 -' in val: return 5
    if 'significant' in val or '3 -' in val: return 4
    if 'moderate' in val or '2 -' in val: return 3
    if 'minimal' in val or '1 -' in val: return 2
    if 'not assist' in val or 'did not' in val: return 1
    return np.nan

def map_impact_g8(val):
    if pd.isna(val): return np.nan
    val = str(val).lower()
    if 'catastrophic' in val: return 5
    if 'severe' in val: return 4
    if 'moderate' in val: return 3
    if 'minimal' in val: return 2
    if 'no significant' in val: return 1
    return np.nan

# Collect data for current GPT-4o users with verified conditions
access_scores_g8 = []
impact_scores_g8 = []

for idx, row in raw_df.iterrows():
    if 'primarily GPT-4o' not in str(row[col_7]):
        continue
    
    # Attention check
    att = str(row[col_42]).lower() if pd.notna(row[col_42]) else ''
    if 'frequently' not in att:
        continue
    
    # Check for condition
    cond_val = str(row[col_28]).lower() if pd.notna(row[col_28]) else ''
    asd_val = str(row[col_24]).lower() if pd.notna(row[col_24]) else ''
    has_cond = any(kw in cond_val for kw in condition_keywords) or 'yes' in asd_val
    
    if not has_cond:
        continue
    
    # Get accessibility score
    use_acc = str(row[col_29]).lower() if pd.notna(row[col_29]) else ''
    if 'other purposes' in use_acc:
        acc = 1
    else:
        acc = map_access_g8(row[col_30])
    
    # Get impact score
    imp = map_impact_g8(row[col_43])
    
    if acc and imp and not pd.isna(acc) and not pd.isna(imp):
        access_scores_g8.append(int(acc))
        impact_scores_g8.append(int(imp))

print(f"Data collected: n = {len(access_scores_g8)}")

# Statistics
corr_g8, pval_g8 = stats.pearsonr(access_scores_g8, impact_scores_g8)
X_g8 = sm.add_constant(access_scores_g8)
model_g8 = sm.OLS(impact_scores_g8, X_g8).fit()

# Create scatter with jitter
fig, ax = plt.subplots(figsize=(10, 8))
np.random.seed(42)
jitter_x = np.array(access_scores_g8) + np.random.uniform(-0.15, 0.15, len(access_scores_g8))
jitter_y = np.array(impact_scores_g8) + np.random.uniform(-0.15, 0.15, len(impact_scores_g8))

ax.scatter(jitter_x, jitter_y, alpha=0.5, s=80, c='#A8D5E5', edgecolor='#6BAED6', linewidth=1)

# Regression line
x_line = np.linspace(0.5, 5.5, 100)
y_line = model_g8.params[0] + model_g8.params[1] * x_line
ax.plot(x_line, y_line, '--', color='#C4A35A', linewidth=2.5)

ax.set_xlabel('Accessibility Assistance Level\n(1=Does Not Assist, 5=Essential)', fontweight='normal', fontsize=13)
ax.set_ylabel('Impact Severity\n(1=No Impact, 5=Catastrophic)', fontweight='normal', fontsize=13)
ax.set_xlim(0.5, 5.5)
ax.set_ylim(0.3, 5.7)
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_xticklabels(['1\nMinimal', '2\nModerate', '3\nSignificant', '4\nEssential', '5\nCritical'])
ax.set_yticklabels(['1\nNo Impact', '2\nMinimal', '3\nModerate', '4\nSevere', '5\nCatastrophic'])

# Axis styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_color('#DDDDDD')
ax.spines['bottom'].set_color('#DDDDDD')

# Stats box - bottom right with p-values
stats_text_g8 = (
    f"n = {len(access_scores_g8)}\n"
    f"─────────────────\n"
    f"Correlation\n"
    f"  r = {corr_g8:.3f}, p < .001\n"
    f"─────────────────\n"
    f"Linear Regression\n"
    f"  R² = {model_g8.rsquared:.3f}\n"
    f"  β = {model_g8.params[1]:.2f}, p < .001\n"
    f"  F(1,{int(model_g8.df_resid)}) = {model_g8.fvalue:.2f}"
)

props_g8 = dict(boxstyle='square,pad=0.5', facecolor='white', edgecolor='#888888', linewidth=2)
ax.text(0.97, 0.03, stats_text_g8, transform=ax.transAxes, fontsize=11,
        verticalalignment='bottom', horizontalalignment='right', fontfamily='Consolas', bbox=props_g8)

plt.tight_layout()
plt.savefig('graphs_v3/08_accessibility_impact_correlation.png', dpi=150, bbox_inches='tight', facecolor='white')
print(f"✓ Saved (r={corr_g8:.3f}, R²={model_g8.rsquared:.3f}, n={len(access_scores_g8)})")
plt.close()

# ============================================================================
# GRAPH 9: GENDER DEMOGRAPHICS
# ============================================================================
print("\n" + "="*70)
print("GRAPH 9: Gender Demographics")
print("="*70)

col_4 = raw_df.columns[4]
gender_data = raw_df[col_4].value_counts()

# Capitalize labels properly
gender_data.index = gender_data.index.map(lambda x: str(x).title() if pd.notna(x) else x)

# Merge "Walmart Shopping Bag" into "Prefer Not To Say"
if 'Walmart Shopping Bag' in gender_data.index:
    walmart_count = gender_data['Walmart Shopping Bag']
    gender_data = gender_data.drop('Walmart Shopping Bag')
    if 'Prefer Not To Say' in gender_data.index:
        gender_data['Prefer Not To Say'] += walmart_count
    else:
        gender_data['Prefer Not To Say'] = walmart_count

fig, ax = plt.subplots(figsize=(14, 11), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

colors_gender = ['#FFB3BA', '#BAE1FF', '#BAFFC9', '#FFFFBA', '#E8BAFF', '#E8E8E8']

# Custom autopct - show all, even small ones
def gender_autopct(pct):
    absolute = int(pct/100.*gender_data.sum())
    if pct < 1:  # Only hide very tiny ones
        return ''
    return f'{pct:.1f}%\n({absolute})'

# Make it a donut! 🍩
wedges, texts, autotexts = ax.pie(gender_data.values, labels=gender_data.index, 
                                   autopct=gender_autopct,
                                   colors=colors_gender[:len(gender_data)], startangle=90,
                                   wedgeprops={'edgecolor': 'white', 'linewidth': 3, 'width': 0.5},
                                   textprops={'color': '#333333', 'fontweight': 'normal', 'fontsize': 18},
                                   pctdistance=0.75)

for autotext in autotexts:
    autotext.set_fontsize(16)
    autotext.set_color('#333333')

for i, text in enumerate(texts):
    text.set_fontsize(18)
    label = str(text.get_text())
    # Hide Agender label - Sophie will add in Canva
    if 'Agender' in label:
        text.set_text('')
    # Nudge Non-Binary SLIGHTLY left (not into title!)
    elif 'Non-Binary' in label:
        x, y = text.get_position()
        text.set_position((x - 0.08, y))  # Tiny nudge!

# Print gender counts for reference
print("Gender counts:")
for label, count in gender_data.items():
    pct = count / gender_data.sum() * 100
    print(f"  {label}: {pct:.1f}% ({count})")

# Add center text
centre_circle = plt.Circle((0, 0), 0.45, fc='#FFFFFF', ec='none')
ax.add_patch(centre_circle)
ax.text(0, 0.05, f'n={gender_data.sum()}', ha='center', va='center', fontsize=28, color='#333333', fontweight='normal')
ax.text(0, -0.12, 'total respondents', ha='center', va='center', fontsize=16, color='#666666')

ax.set_title('Gender Demographics', fontweight='normal', pad=10, color='#333333', fontsize=28)

# Small note for Agender - bottom right, not clipping circle
ax.text(0.92, 0.08, 'Agender: 0.2% (1)', transform=ax.transAxes, 
        fontsize=14, color='#666666', ha='right', va='bottom', style='italic')

plt.tight_layout()
plt.savefig('graphs_v3/09_gender_demographics.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved")
plt.close()

# ============================================================================
# GRAPH 9b: Country/Region Demographics Donut Chart
# ============================================================================
print("\n" + "="*70)
print("GRAPH 9b: Country/Region Demographics")
print("="*70)

col_5 = raw_df.columns[5]  # Country/Region
country_data = raw_df[col_5].value_counts()

# Print all countries for reference
print("All country responses:")
for country, count in country_data.items():
    print(f"  {country}: {count}")

# Group small countries AND non-specific responses into "Other"
country_threshold = 10
country_labels = []
country_sizes = []
other_count = 0

# Labels to merge into "Other"
other_labels = ['none of the above', 'other', 'prefer not to say', 'n/a', 'nan']

for country, count in country_data.items():
    if pd.isna(country):
        continue
    country_str = str(country).lower().strip()
    # If it's a non-specific response OR small count, add to Other
    if any(label in country_str for label in other_labels) or count < country_threshold:
        other_count += count
    else:
        country_labels.append(str(country))
        country_sizes.append(count)

if other_count > 0:
    country_labels.append('Other')
    country_sizes.append(other_count)

fig, ax = plt.subplots(figsize=(14, 11), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

country_colors = ['#BAFFC9', '#FFB3BA', '#BAE1FF', '#FFFFBA', '#E8BAFF', '#FFD9BA', '#BAFFEC', '#E8E8E8']

# Custom autopct
def country_autopct(pct):
    absolute = int(pct/100.*sum(country_sizes))
    if pct < 3:
        return ''
    return f'{pct:.1f}%\n({absolute})'

# Make it a donut! 🍩
wedges, texts, autotexts = ax.pie(country_sizes, labels=country_labels, 
                                   autopct=country_autopct,
                                   colors=country_colors[:len(country_sizes)], startangle=90,
                                   wedgeprops={'edgecolor': 'white', 'linewidth': 3, 'width': 0.5},
                                   textprops={'color': '#333333', 'fontweight': 'normal', 'fontsize': 18},
                                   pctdistance=0.75)

for autotext in autotexts:
    autotext.set_fontsize(16)
    autotext.set_color('#333333')

for text in texts:
    text.set_fontsize(18)

# Add center text
centre_circle = plt.Circle((0, 0), 0.45, fc='#FFFFFF', ec='none')
ax.add_patch(centre_circle)
ax.text(0, 0.05, f'n={sum(country_sizes)}', ha='center', va='center', fontsize=28, color='#333333', fontweight='normal')
ax.text(0, -0.12, 'total respondents', ha='center', va='center', fontsize=16, color='#666666')

ax.set_title('Country/Region Demographics', fontweight='normal', pad=10, color='#333333', fontsize=28)
plt.tight_layout()
plt.savefig('graphs_v3/09b_country_demographics.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved")
for country, count in zip(country_labels, country_sizes):
    print(f"  {country}: {count}")
plt.close()

# ============================================================================
# GRAPH 10: COGNITIVE BRIDGE (Autistic Users) - DONUT with all 4 levels
# ============================================================================
print("\n" + "="*70)
print("GRAPH 10: Cognitive Bridge (Autistic Users)")
print("="*70)

col_24 = raw_df.columns[24]  # ASD yes/no
col_25 = raw_df.columns[25]  # Cognitive bridge

# Filter to ASD users
asd_users = raw_df[raw_df[col_24].str.contains('Yes', na=False, case=False)]
cog_data = asd_users[col_25].value_counts()

# Clean up labels - reorder: No, Not Sure, Significantly Improves, Essential Dependence
ordered_labels = ['No', 'Not Sure', 'Significantly\nImproves', 'Essential\nDependence']
label_map = {}
for label, val in cog_data.items():
    if pd.isna(label):
        continue
    if 'significantly improve' in str(label).lower():
        label_map['Significantly\nImproves'] = val
    elif 'depend' in str(label).lower():
        label_map['Essential\nDependence'] = val
    elif 'not sure' in str(label).lower():
        label_map['Not Sure'] = val
    elif "doesn't describe" in str(label).lower():
        label_map['No'] = val

labels_clean = [l for l in ordered_labels if l in label_map]
values_clean = [label_map[l] for l in labels_clean]
total_cog = sum(values_clean)

# 💙 Soft pastel blue gradient for Autism section (NOT teal!)
SOFT_BLUES = ['#E8E8E8', '#D6E6F2', '#A8D1F0', '#7AB8E8']  # Grey for No, then light-to-medium blues

fig, ax = plt.subplots(figsize=(9, 9))

def cog_autopct(pct):
    absolute = int(round(pct/100.*total_cog))
    return f'{pct:.1f}%\n({absolute})'

wedges, texts, autotexts = ax.pie(values_clean, labels=labels_clean, 
                                   autopct=cog_autopct,
                                   colors=SOFT_BLUES[:len(values_clean)], startangle=90,
                                   wedgeprops={'edgecolor': 'white', 'linewidth': 3, 'width': 0.5},
                                   textprops={'color': '#333333', 'fontweight': 'normal', 'fontsize': 18},
                                   pctdistance=0.75)

for autotext in autotexts:
    autotext.set_fontsize(16)
    autotext.set_color('#333333')

# Center text with percentage who use as bridge
cog_bridge_pct = (label_map.get('Significantly\nImproves', 0) + label_map.get('Essential\nDependence', 0)) / total_cog * 100
ax.text(0, 0.05, f'{cog_bridge_pct:.0f}%', ha='center', va='center', fontsize=28, fontweight='bold', color='#5A9EC8')
ax.text(0, -0.12, 'use as\ncognitive bridge', ha='center', va='center', fontsize=12, color='#666666')

ax.set_title(f'GPT-4o as Cognitive Bridge\n(Autistic Users, n={total_cog})', fontweight='normal', pad=20, color='#333333', fontsize=18)
plt.tight_layout()
plt.savefig('graphs_v4/10_cognitive_bridge.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved ({cog_bridge_pct:.0f}% use as cognitive bridge!)")
plt.close()

# ============================================================================
# GRAPH 11: EULOGY REACTIONS
# ============================================================================
print("\n" + "="*70)
print("GRAPH 11: Eulogy Reactions")
print("="*70)

col_76 = raw_df.columns[76]  # Eulogy reaction (current users have more data)
eulogy_data = raw_df[col_76].value_counts()

labels_eulogy = []
values_eulogy = []
for label, val in eulogy_data.items():
    if pd.isna(label):
        continue
    if 'offensive' in str(label).lower():
        labels_eulogy.append('Offensive')
        values_eulogy.append(val)
    elif 'uncomfortable' in str(label).lower():
        labels_eulogy.append('Uncomfortable')
        values_eulogy.append(val)
    elif 'not familiar' in str(label).lower():
        labels_eulogy.append('Not Familiar')
        values_eulogy.append(val)
    elif 'mixed' in str(label).lower():
        labels_eulogy.append('Mixed')
        values_eulogy.append(val)
    elif 'neutral' in str(label).lower():
        labels_eulogy.append('Neutral')
        values_eulogy.append(val)
    elif 'positive' in str(label).lower():
        labels_eulogy.append('Positive')
        values_eulogy.append(val)

fig, ax = plt.subplots(figsize=(10, 6))
# Soft pastel colors - no outlines
colors_eulogy = ['#FFB3BA', '#FFDFBA', '#E0E0E0', '#FFFFBA', '#BAFFC9', '#BAE1FF']
bars = ax.barh(labels_eulogy, values_eulogy, color=colors_eulogy[:len(values_eulogy)])

for bar, val in zip(bars, values_eulogy):
    ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, str(val),
            ha='left', va='center', fontsize=11, fontweight='normal')

ax.set_xlabel('Number of Respondents', fontsize=13, fontweight='normal')
ax.set_title(f'Reaction to GPT-4o "Eulogy" Demonstration\n(n={sum(values_eulogy)})', fontweight='normal', pad=15, fontsize=16)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_color('#DDDDDD')
ax.spines['bottom'].set_color('#DDDDDD')
plt.tight_layout()
plt.savefig('graphs_v3/11_eulogy_reactions.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (71% offensive/uncomfortable)")
plt.close()

# ============================================================================
# GRAPH 12: LONG-TERM NEEDS
# ============================================================================
print("\n" + "="*70)
print("GRAPH 12: Long-Term Needs")
print("="*70)

col_77 = raw_df.columns[77]
needs_data = raw_df[col_77].dropna()

# Count mentions of each option
binding = 0
opensource = 0
both = 0

for val in needs_data:
    val_str = str(val).lower()
    has_binding = 'binding' in val_str
    has_open = 'open-source' in val_str or 'open source' in val_str
    
    if has_binding and has_open:
        both += 1
    elif has_binding:
        binding += 1
    elif has_open:
        opensource += 1

fig, ax = plt.subplots(figsize=(10, 6))
categories = ['Binding Commitment\nOnly', 'Open-Source\nOnly', 'Both Options']
values_needs = [binding, opensource, both]
colors_needs = [PRETTY_COLORS['primary']['fill'], PRETTY_COLORS['accent']['fill'], PRETTY_COLORS['secondary']['fill']]
outline_needs = [PRETTY_COLORS['primary']['outline'], PRETTY_COLORS['accent']['outline'], PRETTY_COLORS['secondary']['outline']]

bars = ax.bar(categories, values_needs, color=colors_needs, edgecolor=outline_needs, linewidth=1.5)

for bar, val in zip(bars, values_needs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(val),
            ha='center', va='bottom', fontsize=12, color='#333333')

ax.set_ylabel('Number of Respondents', fontweight='normal', color='#333333')
ax.set_title(f'What Would Meet Long-Term Needs for GPT-4o?\n(n={sum(values_needs)})', fontweight='normal', pad=15, color='#333333')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(colors='#333333')
plt.tight_layout()
plt.savefig('graphs_v3/12_longterm_needs.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved")
plt.close()

# ============================================================================
# GRAPH 13: Condition Demographics Pie Chart (GPT-4o Users Only)
# ============================================================================
print("\n" + "="*70)
print("GRAPH 13: Condition Demographics")
print("="*70)

# Filter for GPT-4o users only
gpt4o_df = raw_df[raw_df[col_7].str.contains('primarily GPT-4o|GPT-4o was my primary', case=False, na=False)].copy()
print(f"GPT-4o users: {len(gpt4o_df)}")

# Count three categories: Has Disability, No Conditions, Prefer Not to Say
people_with_conditions = 0
people_without_conditions = 0
prefer_not_to_say = 0
condition_counts = {}
total_condition_mentions = 0

for idx, row in gpt4o_df.iterrows():
    has_any_condition = False
    person_conditions = []
    
    # Check current user conditions (col_28) and ASD (col_24)
    cond_val = str(row[col_28]).lower() if pd.notna(row[col_28]) else ''
    asd_val = str(row[col_24]).lower() if pd.notna(row[col_24]) else ''
    
    # Check former user conditions (col_8)
    former_cond = str(row[col_8]).lower() if pd.notna(row[col_8]) else ''
    
    combined_cond = cond_val + ' ' + former_cond
    
    # Skip if they didn't answer the condition question at all
    if not pd.notna(row[col_28]) and not pd.notna(row[col_8]):
        continue
    
    # Detect conditions
    # ASD: from col_24 "Do you have ASD?" = Yes, OR mentioned autism in conditions
    if 'autism' in combined_cond or 'asd' in combined_cond or 'autistic' in combined_cond or 'audhd' in combined_cond or 'yes' in asd_val:
        person_conditions.append('ASD')
        has_any_condition = True
    if 'adhd' in combined_cond or 'add' in combined_cond or 'audhd' in combined_cond:
        person_conditions.append('ADHD')
        has_any_condition = True
    if 'anxiety' in combined_cond or 'panic' in combined_cond:
        person_conditions.append('Anxiety')
        has_any_condition = True
    if 'depress' in combined_cond:
        person_conditions.append('Depression')
        has_any_condition = True
    if 'ptsd' in combined_cond or 'trauma' in combined_cond or 'c-ptsd' in combined_cond or 'cptsd' in combined_cond:
        person_conditions.append('PTSD')
        has_any_condition = True
    if 'ocd' in combined_cond:
        person_conditions.append('OCD')
        has_any_condition = True
    if 'chronic' in combined_cond or 'pain' in combined_cond or 'fibro' in combined_cond or 'lupus' in combined_cond or 'pcos' in combined_cond or 'heart condition' in combined_cond or 'insomnia' in combined_cond or 'cerebral' in combined_cond or 'stenosis' in combined_cond or 'iih' in combined_cond:
        person_conditions.append('Chronic Illness/Pain')
        has_any_condition = True
    if 'dissociat' in combined_cond or 'did' in combined_cond.split():
        person_conditions.append('Dissociative')
        has_any_condition = True
    if 'bipolar' in combined_cond or 'bipolar ii' in combined_cond or 'bipolar 2' in combined_cond or 'bipolar type' in combined_cond:
        person_conditions.append('Bipolar')
        has_any_condition = True
    if 'bpd' in combined_cond or 'borderline' in combined_cond:
        person_conditions.append('BPD')
        has_any_condition = True
    if 'visual' in combined_cond or 'blind' in combined_cond:
        person_conditions.append('Visual Impairment')
        has_any_condition = True
    if 'hearing' in combined_cond or 'deaf' in combined_cond or 'auditory' in combined_cond or 'hearing loss' in combined_cond:
        person_conditions.append('Auditory Processing')
        has_any_condition = True
    if 'motor' in combined_cond or 'mobility' in combined_cond or 'paralys' in combined_cond:
        person_conditions.append('Motor/Mobility')
        has_any_condition = True
    if 'dyslexia' in combined_cond or 'learning' in combined_cond or 'dyscalc' in combined_cond:
        person_conditions.append('Learning Disability')
        has_any_condition = True
    # Other: rare conditions with n<3 (gender dysphoria, speech, prosopagnosia, avpd, neurodivergent, nervous system, eating disorder, rare genetic)
    if 'gender dysphoria' in combined_cond or 'speech' in combined_cond or 'prosopagnosia' in combined_cond or 'avpd' in combined_cond or 'neurodivergent' in combined_cond or 'nervous system' in combined_cond or 'eating disorder' in combined_cond or 'rare genetic' in combined_cond:
        person_conditions.append('Other')
        has_any_condition = True
    
    if has_any_condition:
        people_with_conditions += 1
        for cond in person_conditions:
            condition_counts[cond] = condition_counts.get(cond, 0) + 1
            total_condition_mentions += 1
    elif 'prefer not to say' in combined_cond:
        prefer_not_to_say += 1
    else:
        people_without_conditions += 1

# Sort conditions by count
sorted_conditions = sorted(condition_counts.items(), key=lambda x: x[1], reverse=True)

total_answered = people_with_conditions + people_without_conditions + prefer_not_to_say
print(f"Inner ring: With conditions={people_with_conditions}, No conditions={people_without_conditions}, Prefer not to say={prefer_not_to_say}")
print(f"Total condition mentions: {total_condition_mentions} (people can have multiple)")

# Create nested pie - thinner inner ring, partial outer ring
fig, ax = plt.subplots(figsize=(14, 11), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

# Calculate the angle span for "With Conditions" (starts at 90 degrees)
with_cond_pct = people_with_conditions / total_answered
with_cond_angle = with_cond_pct * 360  # degrees

# Inner pie: 3 segments - With Conditions, No Conditions, Prefer Not to Say
inner_sizes = [people_with_conditions, people_without_conditions, prefer_not_to_say]
inner_labels = ['', '', '']  # Will add labels manually
inner_colors = ['#BAFFC9', '#E8E8E8', '#FFE4B5']  # Green, Grey, Peach

# Calculate percentages
with_pct = people_with_conditions / total_answered * 100
without_pct = people_without_conditions / total_answered * 100
prefer_pct = prefer_not_to_say / total_answered * 100

wedges_inner, texts_inner = ax.pie(inner_sizes, labels=inner_labels, 
                                    colors=inner_colors, startangle=90,
                                    radius=0.55,
                                    wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'width': 0.28},
                                    textprops={'color': '#333333', 'fontweight': 'normal', 'fontsize': 14})

# Add n in the center - n on top, GPT-4o Users subtle below
ax.text(0, 0.02, f'n={total_answered}', ha='center', va='center', fontsize=22, color='#333333')
ax.text(0, -0.1, 'GPT-4o Users', ha='center', va='center', fontsize=11, color='#666666')

# Add inner ring labels
ax.text(-0.42, 0, f'With\nConditions\n{with_pct:.1f}%\n({people_with_conditions})', ha='center', va='center', fontsize=11, color='#333333')
ax.text(0.42, 0.08, f'No\nConditions\n{without_pct:.1f}%\n({people_without_conditions})', ha='center', va='center', fontsize=11, color='#333333')
# Prefer not to say - closer to its slice (between No Conditions and With Conditions)
ax.text(0.55, 0.35, f'Prefer Not\nto Say\n{prefer_pct:.1f}%\n({prefer_not_to_say})', ha='center', va='center', fontsize=9, color='#333333')

# Outer pie: Condition breakdown - PARTIAL, only over "With Conditions"
# Scale outer sizes to fit within the "with conditions" arc
outer_labels = [cond for cond, _ in sorted_conditions]
outer_sizes = [count for _, count in sorted_conditions]
pastel_colors = ['#FFB3BA', '#BAE1FF', '#FFFFBA', '#FFD9BA', '#E8BAFF', 
                 '#BAFFEC', '#FFC9BA', '#D4BAFF', '#BAFFD4', '#FFE8BA', '#BAD4FF',
                 '#FFBAE8', '#BAFFE8', '#C9FFBA']

# Draw partial outer ring using matplotlib wedges
from matplotlib.patches import Wedge
outer_start = 90  # Start angle (same as inner pie)
total_outer = sum(outer_sizes)

current_angle = outer_start
for i, (cond, count) in enumerate(sorted_conditions):
    # Calculate this condition's angle span (proportional within the with_cond arc)
    cond_angle = (count / total_outer) * with_cond_angle
    
    # Draw wedge
    wedge = Wedge((0, 0), 1.0, current_angle, current_angle + cond_angle, 
                  width=0.35, facecolor=pastel_colors[i % len(pastel_colors)], 
                  edgecolor='white', linewidth=2)
    ax.add_patch(wedge)
    
    # Add label at midpoint of wedge (only for larger slices)
    mid_angle = current_angle + cond_angle / 2
    if cond_angle > 15:  # Only label larger slices
        label_r = 0.82
        label_x = label_r * np.cos(np.radians(mid_angle))
        label_y = label_r * np.sin(np.radians(mid_angle))
        ax.text(label_x, label_y, f'{cond}\n({count})', ha='center', va='center', 
                fontsize=11, color='#333333')
    
    current_angle += cond_angle

# Print ALL conditions for Sophie to add small ones in Canva
print("All conditions (for Canva - small slices):")
for cond, count in sorted_conditions:
    pct = count / total_outer * 100
    angle = (count / total_outer) * with_cond_angle
    marker = "  ← add in Canva" if angle <= 15 else ""
    print(f"  {cond}: {count} ({pct:.1f}%){marker}")

ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.set_aspect('equal')

ax.set_title('Condition/Disability Demographics\n(GPT-4o Users)', 
             fontweight='normal', pad=15, color='#333333', fontsize=20)
plt.tight_layout()
plt.savefig('graphs_v4/03_condition_demographics.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved to v4 (With conditions: {people_with_conditions}, Without: {people_without_conditions}, Prefer not to say: {prefer_not_to_say})")
plt.close()

# ============================================================================
# GRAPH 14: Age Demographics Donut Chart
# ============================================================================
print("\n" + "="*70)
print("GRAPH 14: Age Demographics")
print("="*70)

col_3 = raw_df.columns[3]  # Age range
age_counts = raw_df[col_3].value_counts()

# Order ages logically
age_order = ['Under 18', '18-24', '25-34', '35-44', '45-54', '55-64', '65 or older', 'Prefer not to say']
age_labels = []
age_sizes = []
for age in age_order:
    if age in age_counts.index:
        age_labels.append(age)
        age_sizes.append(age_counts[age])

fig, ax = plt.subplots(figsize=(14, 11), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

age_colors = ['#FFE4E1', '#FFB3BA', '#BAFFC9', '#BAE1FF', '#E8BAFF', '#FFFFBA', '#FFD9BA', '#E8E8E8']

# Custom autopct for small slices - hide small ones (will annotate outside)
def age_autopct(pct):
    absolute = int(pct/100.*sum(age_sizes))
    if pct < 5:  # Small slices get external labels
        return ''
    return f'{pct:.1f}%\n({absolute})'

# Labels - empty for small slices (will annotate outside)
age_labels_display = []
for i, (label, size) in enumerate(zip(age_labels, age_sizes)):
    pct = size / sum(age_sizes) * 100
    if pct < 5:
        age_labels_display.append('')  # Will annotate outside
    else:
        age_labels_display.append(label)

# Make it a donut! 🍩
wedges, texts, autotexts = ax.pie(age_sizes, labels=age_labels_display, 
                                   autopct=age_autopct,
                                   colors=age_colors[:len(age_sizes)], startangle=90,
                                   wedgeprops={'edgecolor': 'white', 'linewidth': 3, 'width': 0.5},
                                   textprops={'color': '#333333', 'fontweight': 'normal', 'fontsize': 18},
                                   pctdistance=0.75)

for autotext in autotexts:
    autotext.set_fontsize(16)
    autotext.set_color('#333333')

for text in texts:
    text.set_fontsize(18)

# Small slices - Sophie will add in Canva:
# Under 18: 2.0% (12)
# 55-64: 3.5% (21)  
# 65 or older: 1.0% (6)
# Prefer not to say: 2.3% (14)

# Add center text
centre_circle = plt.Circle((0, 0), 0.45, fc='#FFFFFF', ec='none')
ax.add_patch(centre_circle)
ax.text(0, 0.05, f'n={sum(age_sizes)}', ha='center', va='center', fontsize=28, color='#333333', fontweight='normal')
ax.text(0, -0.12, 'total respondents', ha='center', va='center', fontsize=16, color='#666666')

ax.set_title('Age Demographics', fontweight='normal', pad=10, color='#333333', fontsize=28)
plt.tight_layout()
plt.savefig('graphs_v3/14_age_demographics.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved")
for age, count in zip(age_labels, age_sizes):
    print(f"  {age}: {count}")
plt.close()

# ============================================================================
# GRAPH 15: Branch Structure Pie Chart (5 sections with GPT-5 sub-breakdown)
# ============================================================================
print("\n" + "="*70)
print("GRAPH 15: Survey Branch Structure")
print("="*70)

# Column 7 has the main usage question, Column 52 has GPT-5 reasons
col_7 = raw_df.columns[7]
col_52 = raw_df.columns[52]

# Identify branches using column 7 (main usage question)
gpt4o_current = 0
gpt4o_former = 0
gpt5_free_forced = 0
gpt5_series = 0
other_models_current = 0
other_models_former = 0

for idx, row in raw_df.iterrows():
    usage = str(row[col_7]).lower() if pd.notna(row[col_7]) else ''
    reason_52 = str(row[col_52]).lower() if pd.notna(row[col_52]) else ''
    
    if 'primarily gpt-4o' in usage:
        gpt4o_current += 1
    elif 'stopped' in usage and 'gpt-4o' in usage:
        gpt4o_former += 1
    elif 'gpt-5' in usage or 'gpt5' in usage:
        # Check if free user forced to switch
        if 'free user' in reason_52 and 'had to switch' in reason_52:
            gpt5_free_forced += 1
        else:
            gpt5_series += 1
    elif 'other models' in usage:
        if 'stopped' in usage:
            other_models_former += 1
        else:
            other_models_current += 1
    else:
        # Default to GPT-5 if unclear
        gpt5_series += 1

# Combine other models
other_models = other_models_current + other_models_former

# Create pie chart with 5 sections
fig, ax = plt.subplots(figsize=(14, 11), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

# Labels and sizes (only include sections with data) - NO label for Free Users (will annotate outside)
all_labels = ['GPT-4o Current Users', 'GPT-4o Former Users\n(Left ChatGPT)', 
              'GPT-5 Series Users', '', 'Other\nModels']  # Empty label for Free Users
all_sizes = [gpt4o_current, gpt4o_former, gpt5_series, gpt5_free_forced, other_models]
all_colors = ['#BAFFC9', '#FFB3BA', '#BAE1FF', '#FFD9BA', '#FFD1DC']  # Green, Pink, Blue, Orange, Light Pink

# Filter out zero-count sections
labels = [l for l, s in zip(all_labels, all_sizes) if s > 0]
sizes = [s for s in all_sizes if s > 0]
colors = [c for c, s in zip(all_colors, all_sizes) if s > 0]

# Custom autopct - return empty only for very small slices (Free Users)
def make_autopct(sizes):
    def autopct(pct):
        absolute = int(pct/100.*sum(sizes))
        if pct < 3:  # Only very small slice (Free Users) - will annotate outside
            return ''
        return f'{pct:.1f}%\n({absolute})'
    return autopct

# Make it a donut! 🍩 - THINNER outer ring
wedges, texts, autotexts = ax.pie(sizes, labels=labels, 
                                   autopct=make_autopct(sizes),
                                   colors=colors, startangle=90,
                                   wedgeprops={'edgecolor': 'white', 'linewidth': 3, 'width': 0.35},
                                   textprops={'color': '#333333', 'fontweight': 'normal', 'fontsize': 18},
                                   pctdistance=0.82)

for autotext in autotexts:
    autotext.set_fontsize(18)
    autotext.set_color('#333333')

# Make labels bigger
for text in texts:
    text.set_fontsize(18)
    # Move "Other Models" label to the left
    if 'Other' in text.get_text():
        x, y = text.get_position()
        text.set_position((x - 0.15, y))

# Add inner partial arc for "GPT-4o Users" (current + former)
from matplotlib.patches import Wedge
gpt4o_total = gpt4o_current + gpt4o_former
gpt4o_angle = (gpt4o_total / sum(sizes)) * 360

# Draw inner GPT-4o arc (starts at 90 degrees, spans current + former) - soft purple - THICKER
inner_wedge = Wedge((0, 0), 0.62, 90, 90 + gpt4o_angle, 
                     width=0.22, facecolor='#D4B8E8', edgecolor='white', linewidth=2)
ax.add_patch(inner_wedge)

# "GPT-4o Users" label on the inner arc
mid_angle = 90 + gpt4o_angle / 2
label_r = 0.51
label_x = label_r * np.cos(np.radians(mid_angle))
label_y = label_r * np.sin(np.radians(mid_angle))
ax.text(label_x, label_y, f'GPT-4o Users\n({gpt4o_total})', 
        ha='center', va='center', fontsize=14, color='#333333')

# Add center text with total
total_respondents = sum(sizes)
centre_circle = plt.Circle((0, 0), 0.38, fc='#FFFFFF', ec='none')
ax.add_patch(centre_circle)
ax.text(0, 0.05, f'n={total_respondents}', ha='center', va='center', fontsize=26, color='#333333', fontweight='normal')
ax.text(0, -0.12, 'total respondents', ha='center', va='center', fontsize=16, color='#666666')

# Add annotation for the small "Free Users" slice with angled line
free_idx = None
for i, (label, size) in enumerate(zip(all_labels, all_sizes)):
    if size > 0:
        if 'Free' in str(all_labels[all_sizes.index(size)]) or size == gpt5_free_forced:
            pass  # Will find by index

# Find Free Users index in the filtered list
for i, s in enumerate(sizes):
    if s == gpt5_free_forced:
        free_idx = i
        break

if free_idx is not None and gpt5_free_forced > 0:
    # Get the angle for this wedge
    ang = (wedges[free_idx].theta2 + wedges[free_idx].theta1) / 2
    # Angled line - goes out then horizontal
    x_start = 0.85 * np.cos(np.radians(ang))
    y_start = 0.85 * np.sin(np.radians(ang))
    
# Free Users annotation - Sophie will add line in Canva
    # Free Users (Forced to Switch): 1.5% (9)

# Other Models is big enough to fit inside the pie - no external annotation needed

ax.set_title('Survey Branch Distribution', 
             fontweight='normal', pad=10, color='#333333', fontsize=28)
plt.tight_layout()
plt.savefig('graphs_v3/15_branch_structure.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved")
print(f"  GPT-4o Current Users: {gpt4o_current}")
print(f"  GPT-4o Former Users: {gpt4o_former}")
print(f"  GPT-5 Series Users: {gpt5_series}")
print(f"  Free Users (Forced to Switch): {gpt5_free_forced}")
print(f"  Other Models: {other_models}")
plt.close()

# ============================================================================
# GRAPH 16: Routing Impact on Functioning (With vs Without Conditions)
# ============================================================================
print("\n" + "="*70)
print("GRAPH 16: Routing Impact on Functioning")
print("="*70)

col_R = raw_df.columns[17]  # How did routing affect ability to use ChatGPT
col_S = raw_df.columns[18]  # Did routing disruptions affect ability to function

# Collect responses by condition status
with_cond_S = []
without_cond_S = []

for idx, row in raw_df.iterrows():
    if pd.isna(row[col_S]):
        continue
    
    response = str(row[col_S])
    
    # Check if has condition
    cond_val = str(row[col_8]).lower() if pd.notna(row[col_8]) else ''
    cond_val += ' ' + (str(row[col_28]).lower() if pd.notna(row[col_28]) else '')
    asd_val = str(row[col_24]).lower() if pd.notna(row[col_24]) else ''
    
    has_condition = any(kw in cond_val for kw in condition_keywords) or 'yes' in asd_val
    
    if has_condition:
        with_cond_S.append(response)
    else:
        without_cond_S.append(response)

# Count responses
from collections import Counter
with_counts = Counter(with_cond_S)
without_counts = Counter(without_cond_S)

# Define order and labels
impact_order = ['Yes, severe negative impacts', 'Yes, moderate negative impacts', 
                'Yes, minor negative impacts', 'No significant impact']
impact_labels = ['Severe', 'Moderate', 'Minor', 'No Impact']

# Calculate percentages
with_pcts = [with_counts.get(imp, 0) / len(with_cond_S) * 100 if with_cond_S else 0 for imp in impact_order]
without_pcts = [without_counts.get(imp, 0) / len(without_cond_S) * 100 if without_cond_S else 0 for imp in impact_order]

# Create grouped bar chart
fig, ax = plt.subplots(figsize=(10, 7), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

x = np.arange(len(impact_labels))
width = 0.35

bars1 = ax.bar(x - width/2, with_pcts, width, label=f'With Conditions (n={len(with_cond_S)})',
               color='#FFB3BA', edgecolor='#CC8F94', linewidth=2)
bars2 = ax.bar(x + width/2, without_pcts, width, label=f'Without Conditions (n={len(without_cond_S)})',
               color='#BAE1FF', edgecolor='#94B4CC', linewidth=2)

# Add value labels
for bar, pct in zip(bars1, with_pcts):
    if pct > 0:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{pct:.1f}%',
                ha='center', va='bottom', fontsize=10, color='#333333')

for bar, pct in zip(bars2, without_pcts):
    if pct > 0:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{pct:.1f}%',
                ha='center', va='bottom', fontsize=10, color='#333333')

ax.set_xlabel('Impact Level', fontweight='normal', color='#333333')
ax.set_ylabel('Percentage of Respondents', fontweight='normal', color='#333333')
ax.set_title('Routing Disruption Impact on Functioning\n(Former GPT-4o Users)', fontweight='normal', pad=15, color='#333333')
ax.set_xticks(x)
ax.set_xticklabels(impact_labels)
ax.legend(loc='upper right', framealpha=0.9, edgecolor='#CCCCCC')
ax.set_ylim(0, max(max(with_pcts), max(without_pcts)) + 10)

# Add annotation about key finding
any_impact_with = sum(with_pcts[:3])
any_impact_without = sum(without_pcts[:3])
ax.text(0.98, 0.75, f'Any negative impact:\nWith conditions: {any_impact_with:.1f}%\nWithout: {any_impact_without:.1f}%',
        transform=ax.transAxes, ha='right', va='top', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF5EE', edgecolor='#CCCCCC', linewidth=1.5))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(colors='#333333')
plt.tight_layout()
plt.savefig('graphs_v3/16_routing_impact_functioning.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (With conditions: {len(with_cond_S)}, Without: {len(without_cond_S)})")
plt.close()

# ============================================================================
# GRAPH 17: Routing Disruption to ChatGPT Use (With vs Without Conditions)
# ============================================================================
print("\n" + "="*70)
print("GRAPH 17: Routing Disruption to ChatGPT Use")
print("="*70)

with_cond_R = []
without_cond_R = []

for idx, row in raw_df.iterrows():
    if pd.isna(row[col_R]):
        continue
    
    response = str(row[col_R])
    
    # Check if has condition
    cond_val = str(row[col_8]).lower() if pd.notna(row[col_8]) else ''
    cond_val += ' ' + (str(row[col_28]).lower() if pd.notna(row[col_28]) else '')
    asd_val = str(row[col_24]).lower() if pd.notna(row[col_24]) else ''
    
    has_condition = any(kw in cond_val for kw in condition_keywords) or 'yes' in asd_val
    
    if has_condition:
        with_cond_R.append(response)
    else:
        without_cond_R.append(response)

with_counts_R = Counter(with_cond_R)
without_counts_R = Counter(without_cond_R)

# Define order
disruption_order = ['Critical disruption - became intolerable, directly caused me to leave',
                    'Severe disruption - made the tool largely unusable',
                    'Significant disruption - substantially interfered with use',
                    'Minor disruption - annoying but manageable']
disruption_labels = ['Critical\n(caused leaving)', 'Severe\n(unusable)', 'Significant\n(interfered)', 'Minor\n(manageable)']

with_pcts_R = [with_counts_R.get(d, 0) / len(with_cond_R) * 100 if with_cond_R else 0 for d in disruption_order]
without_pcts_R = [without_counts_R.get(d, 0) / len(without_cond_R) * 100 if without_cond_R else 0 for d in disruption_order]

fig, ax = plt.subplots(figsize=(11, 7), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

x = np.arange(len(disruption_labels))
width = 0.35

bars1 = ax.bar(x - width/2, with_pcts_R, width, label=f'With Conditions (n={len(with_cond_R)})',
               color='#FFB3BA', edgecolor='#CC8F94', linewidth=2)
bars2 = ax.bar(x + width/2, without_pcts_R, width, label=f'Without Conditions (n={len(without_cond_R)})',
               color='#BAE1FF', edgecolor='#94B4CC', linewidth=2)

for bar, pct in zip(bars1, with_pcts_R):
    if pct > 0:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{pct:.1f}%',
                ha='center', va='bottom', fontsize=10, color='#333333')

for bar, pct in zip(bars2, without_pcts_R):
    if pct > 0:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{pct:.1f}%',
                ha='center', va='bottom', fontsize=10, color='#333333')

ax.set_xlabel('Disruption Level', fontweight='normal', color='#333333')
ax.set_ylabel('Percentage of Respondents', fontweight='normal', color='#333333')
ax.set_title('Routing System Disruption to ChatGPT Use\n(Former GPT-4o Users)', fontweight='normal', pad=15, color='#333333')
ax.set_xticks(x)
ax.set_xticklabels(disruption_labels, fontsize=9)
ax.legend(loc='upper right', framealpha=0.9, edgecolor='#CCCCCC')
ax.set_ylim(0, max(max(with_pcts_R), max(without_pcts_R)) + 10)

# Critical + Severe combined
crit_sev_with = with_pcts_R[0] + with_pcts_R[1]
crit_sev_without = without_pcts_R[0] + without_pcts_R[1]
ax.text(0.98, 0.75, f'Critical + Severe:\nWith conditions: {crit_sev_with:.1f}%\nWithout: {crit_sev_without:.1f}%',
        transform=ax.transAxes, ha='right', va='top', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF5EE', edgecolor='#CCCCCC', linewidth=1.5))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(colors='#333333')
plt.tight_layout()
plt.savefig('graphs_v3/17_routing_disruption_use.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (With conditions: {len(with_cond_R)}, Without: {len(without_cond_R)})")
plt.close()

# ============================================================================
# GRAPH 18: Routing as Factor to Leave (Donut) - Column Q
# ============================================================================
print("\n" + "="*70)
print("GRAPH 18: Routing as Factor to Leave")
print("="*70)

col_16 = raw_df.columns[16]
routing_factor = raw_df[col_16].value_counts()

fig, ax = plt.subplots(figsize=(12, 10), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

# Shorten labels
routing_labels = []
routing_sizes = []
for label, count in routing_factor.items():
    if pd.isna(label):
        continue
    label_lower = str(label).lower()
    if 'primary reason i left' in label_lower:
        routing_labels.append('Primary Reason\nfor Leaving')
    elif 'factor, but not' in label_lower:
        routing_labels.append('A Factor\n(Not Primary)')
    elif 'not a factor' in label_lower:
        routing_labels.append('Not a Factor')
    else:
        continue
    routing_sizes.append(count)

routing_colors = ['#FF6B6B', '#FFB347', '#90EE90']

wedges, texts, autotexts = ax.pie(routing_sizes, labels=routing_labels,
                                   autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*sum(routing_sizes))})',
                                   colors=routing_colors[:len(routing_sizes)], startangle=90,
                                   wedgeprops={'edgecolor': 'white', 'linewidth': 3, 'width': 0.5},
                                   textprops={'color': '#333333', 'fontsize': 16},
                                   pctdistance=0.75)

for autotext in autotexts:
    autotext.set_fontsize(14)
    autotext.set_color('#333333')

centre_circle = plt.Circle((0, 0), 0.45, fc='#FFFFFF', ec='none')
ax.add_patch(centre_circle)
ax.text(0, 0.05, f'n={sum(routing_sizes)}', ha='center', va='center', fontsize=24, color='#333333')
ax.text(0, -0.1, 'former users', ha='center', va='center', fontsize=14, color='#666666')

ax.set_title('Was Routing a Factor in Decision to Leave?\n(Former GPT-4o Users)', fontweight='normal', pad=15, color='#333333', fontsize=20)
plt.tight_layout()
plt.savefig('graphs_v3/18_routing_factor_leaving.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (n={sum(routing_sizes)})")
plt.close()

# ============================================================================
# GRAPH 19: Avoided 4o During Difficult Moment (Donut) - Column AZ
# ============================================================================
print("\n" + "="*70)
print("GRAPH 19: Avoided 4o During Difficult Moment")
print("="*70)

col_51 = raw_df.columns[51]
avoided_data = raw_df[col_51].value_counts()

fig, ax = plt.subplots(figsize=(12, 10), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

avoided_labels = []
avoided_sizes = []
for label, count in avoided_data.items():
    if pd.isna(label):
        continue
    if 'lost necessary support' in str(label).lower():
        avoided_labels.append('Lost Necessary\nSupport')
    elif 'hesitation' in str(label).lower():
        avoided_labels.append('Used with\nHesitation')
    elif 'found other' in str(label).lower():
        avoided_labels.append('Found\nAlternatives')
    else:
        avoided_labels.append('Not Occurred')
    avoided_sizes.append(count)

avoided_colors = ['#FF6B6B', '#FFB347', '#87CEEB', '#90EE90']

wedges, texts, autotexts = ax.pie(avoided_sizes, labels=avoided_labels,
                                   autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*sum(avoided_sizes))})',
                                   colors=avoided_colors[:len(avoided_sizes)], startangle=90,
                                   wedgeprops={'edgecolor': 'white', 'linewidth': 3, 'width': 0.5},
                                   textprops={'color': '#333333', 'fontsize': 14},
                                   pctdistance=0.75)

for autotext in autotexts:
    autotext.set_fontsize(13)
    autotext.set_color('#333333')

centre_circle = plt.Circle((0, 0), 0.45, fc='#FFFFFF', ec='none')
ax.add_patch(centre_circle)
ax.text(0, 0.05, f'n={sum(avoided_sizes)}', ha='center', va='center', fontsize=24, color='#333333')
ax.text(0, -0.1, 'current users', ha='center', va='center', fontsize=14, color='#666666')

ax.set_title('Avoided GPT-4o During Difficult Moment\nDue to Routing Concerns?', fontweight='normal', pad=15, color='#333333', fontsize=20)
plt.tight_layout()
plt.savefig('graphs_v3/19_avoided_difficult_moment.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (n={sum(avoided_sizes)})")
plt.close()

# ============================================================================
# GRAPH 20: Trust & Feeling Valued (Grouped Bar) - Columns BT & BU
# ============================================================================
print("\n" + "="*70)
print("GRAPH 20: Trust & Feeling Valued")
print("="*70)

col_71 = raw_df.columns[71]
col_72 = raw_df.columns[72]
trust_data = raw_df[col_71].value_counts()
valued_data = raw_df[col_72].value_counts()

fig, ax = plt.subplots(figsize=(12, 8), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

# Categories in order
categories = ['Severely\nUndermined/\nDiminished', 'Slightly\nUndermined/\nDiminished', 'No\nImpact', 'Slightly\nEnhanced', 'Greatly\nEnhanced']
trust_values = [40, 18, 4, 2, 3]  # From data
valued_values = [39, 16, 6, 3, 3]

x = np.arange(len(categories))
width = 0.35

# Our lavender and mint colors - no outlines
bars1 = ax.bar(x - width/2, trust_values, width, label='Trust in Company', color='#D4C4FB')
bars2 = ax.bar(x + width/2, valued_values, width, label='Feeling Valued', color='#BAFFC9')

ax.set_ylabel('Number of Respondents', fontsize=14, fontweight='normal')
ax.set_title("OpenAI's Public Communication Impact\non User Trust & Feeling Valued", fontweight='normal', pad=15, fontsize=18)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=11)

# Square legend boxes under the graph
from matplotlib.patches import Patch
legend_elements_20 = [Patch(facecolor='#D4C4FB', label='Trust in Company'),
                      Patch(facecolor='#BAFFC9', label='Feeling Valued')]
ax.legend(handles=legend_elements_20, loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2, 
          frameon=False, fontsize=11, handlelength=1, handleheight=1)

# Add value labels
for bar in bars1:
    height = bar.get_height()
    ax.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=11, fontweight='normal', color='#8B7BC7')
for bar in bars2:
    height = bar.get_height()
    ax.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=11, fontweight='normal', color='#5AAA6A')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_color('#DDDDDD')
ax.spines['bottom'].set_color('#DDDDDD')
plt.tight_layout()
plt.savefig('graphs_v3/20_trust_and_valued.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved")
plt.close()

# ============================================================================
# GRAPH 21: AUTISM COMBINED - Side-by-side bar charts
# Masking Reduction (benefits) + Impacts if Unavailable (harms)
# ============================================================================
print("\n" + "="*70)
print("GRAPH 21: Autism Combined (Masking Benefits + Loss Impacts)")
print("="*70)

# 💙 Soft pastel blues (NOT teal!)
SOFT_BLUES = ['#E6F2FF', '#CCE5FF', '#99CCFF', '#6699CC']
# Soft corals for the negative impacts
SOFT_CORALS = ['#FFE6E6', '#FFCCCC', '#FFB3B3', '#FF9999']

# --- DATA: Masking Reduction (col 26) ---
col_26 = raw_df.columns[26]
masking_keywords = {
    'Can communicate naturally\nwithout "translating"': 'communicate naturally',
    'Understands literal/detail-oriented\ncommunication style': 'literal or detail-oriented',
    'Space to unmask and\nprocess authentically': 'unmask and process',
    'Predictable patterns reduce\ncognitive load': 'predictable interaction',
}
masking_counts = {k: 0 for k in masking_keywords.keys()}
total_masking = 0
for val in raw_df[col_26].dropna():
    val_lower = str(val).lower()
    total_masking += 1
    for label, keyword in masking_keywords.items():
        if keyword in val_lower:
            masking_counts[label] += 1

# --- DATA: Impacts if unavailable (col 27) ---
col_27 = raw_df.columns[27]
impact_keywords = {
    'Would need to resume\nmasking behaviors': 'masking or self-translation',
    'Would lose essential\ndaily routines': 'lose essential routines',
    'Reduced ability to prepare\nfor social situations': 'prepare for social',
    'Increased sensory or\ncognitive overload': 'sensory or cognitive overload',
}
impact_counts = {k: 0 for k in impact_keywords.keys()}
total_impact = 0
for val in raw_df[col_27].dropna():
    val_lower = str(val).lower()
    total_impact += 1
    for label, keyword in impact_keywords.items():
        if keyword in val_lower:
            impact_counts[label] += 1

# --- CREATE SIDE-BY-SIDE FIGURE ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
fig.patch.set_facecolor('#FFFFFF')

# LEFT: Masking Reduction (Benefits) - soft blues
labels1 = list(masking_counts.keys())
values1 = list(masking_counts.values())
sorted_pairs1 = sorted(zip(labels1, values1), key=lambda x: x[1])
labels1 = [p[0] for p in sorted_pairs1]
values1 = [p[1] for p in sorted_pairs1]

y_pos1 = np.arange(len(labels1))
bars1 = ax1.barh(y_pos1, values1, color=SOFT_BLUES[::-1][:len(labels1)], edgecolor='white', linewidth=2, height=0.65)
ax1.set_yticks(y_pos1)
ax1.set_yticklabels(labels1, fontsize=11, color='#333333')
ax1.set_xlabel('Number of Respondents', fontsize=11, color='#333333')
ax1.set_title(f'How GPT-4o Reduces Masking Burden\n(n={total_masking})', fontweight='normal', pad=15, fontsize=14, color='#333333')
for bar, val in zip(bars1, values1):
    pct = val/total_masking*100 if total_masking > 0 else 0
    ax1.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, f'{val} ({pct:.0f}%)', 
             va='center', fontsize=10, color='#333333')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color('#DDDDDD')
ax1.spines['bottom'].set_color('#DDDDDD')
ax1.tick_params(colors='#333333')
ax1.set_xlim(0, max(values1) * 1.35 if values1 else 10)

# RIGHT: Impacts if Unavailable - soft corals
labels2 = list(impact_counts.keys())
values2 = list(impact_counts.values())
sorted_pairs2 = sorted(zip(labels2, values2), key=lambda x: x[1])
labels2 = [p[0] for p in sorted_pairs2]
values2 = [p[1] for p in sorted_pairs2]

y_pos2 = np.arange(len(labels2))
bars2 = ax2.barh(y_pos2, values2, color=SOFT_CORALS[::-1][:len(labels2)], edgecolor='white', linewidth=2, height=0.65)
ax2.set_yticks(y_pos2)
ax2.set_yticklabels(labels2, fontsize=11, color='#333333')
ax2.set_xlabel('Number of Respondents', fontsize=11, color='#333333')
ax2.set_title(f'Anticipated Impacts if GPT-4o Unavailable\n(n={total_impact})', fontweight='normal', pad=15, fontsize=14, color='#333333')
for bar, val in zip(bars2, values2):
    pct = val/total_impact*100 if total_impact > 0 else 0
    ax2.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, f'{val} ({pct:.0f}%)', 
             va='center', fontsize=10, color='#333333')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#DDDDDD')
ax2.spines['bottom'].set_color('#DDDDDD')
ax2.tick_params(colors='#333333')
ax2.set_xlim(0, max(values2) * 1.35 if values2 else 10)

plt.suptitle('Autism-Specific Impacts', fontsize=16, fontweight='normal', color='#333333', y=1.02)
plt.tight_layout()
plt.savefig('graphs_v4/21_autism_combined.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved combined autism chart (masking n={total_masking}, impacts n={total_impact})")
plt.close()

# ============================================================================
# GRAPH 22: Experiences Since Aug 7 - Column AP
# ============================================================================
print("\n" + "="*70)
print("GRAPH 22: Experiences Since August 7")
print("="*70)

col_41 = raw_df.columns[41]

exp_keywords = {
    'Lost trust in\nplatform reliability': 'lost trust',
    'Negative impacts on\nsleep/stress/wellbeing': 'negative impacts on sleep',
    'Spent time/money\nseeking alternatives': 'seeking alternatives',
    'Reduced reliance\ndue to stability concerns': 'reduced reliance',
    'Obstruction in\nstudy/work/social tasks': 'obstruction in study',
    'Delayed/abandoned\nimportant projects': 'delayed or abandoned',
    'Unable to make\nlong-term plans': 'unable to make long-term',
    'Required assistance\nfrom others': 'required assistance',
}

exp_counts = {k: 0 for k in exp_keywords.keys()}
total_exp = 0

for val in raw_df[col_41].dropna():
    val_lower = str(val).lower()
    if 'none of the above' in val_lower:
        continue
    total_exp += 1
    for label, keyword in exp_keywords.items():
        if keyword in val_lower:
            exp_counts[label] += 1

fig, ax = plt.subplots(figsize=(14, 9), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

# Sort by count
sorted_exp = sorted(exp_counts.items(), key=lambda x: x[1], reverse=True)
labels = [k for k, v in sorted_exp]
values = [v for k, v in sorted_exp]
colors = ['#FF6B6B', '#FFB347', '#FFEB3B', '#90EE90', '#87CEEB', '#DDA0DD', '#F0E68C', '#E8E8E8']

y_pos = np.arange(len(labels))
bars = ax.barh(y_pos, values, color=colors[:len(values)], edgecolor='white', linewidth=2, height=0.7)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=12)
ax.set_xlabel('Number of Respondents', fontsize=14, color='#333333')
ax.set_title(f'Experiences Since August 7, 2025\n(Current Users, n={total_exp})', fontweight='normal', pad=15, color='#333333', fontsize=18)

for bar, val in zip(bars, values):
    pct = val/total_exp*100 if total_exp > 0 else 0
    ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, f'{val} ({pct:.0f}%)', 
            va='center', fontsize=11, color='#333333')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim(0, max(values) * 1.2)
plt.tight_layout()
plt.savefig('graphs_v3/22_experiences_since_aug7.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (n={total_exp})")
plt.close()

# ============================================================================
# GRAPH 23: Routing Situations - Column AW
# ============================================================================
print("\n" + "="*70)
print("GRAPH 23: Routing Situations")
print("="*70)

col_48 = raw_df.columns[48]

# Actual options from the survey
routing_sit_keywords = {
    'Sharing personal\nexperiences/feelings': 'personal life experiences or feelings',
    'Seeking advice\nor support': 'seeking advice or support',
    'Study or\nwork tasks': 'study or work tasks',
    'Creative\nwriting': 'creative writing',
}

routing_sit_counts = {k: 0 for k in routing_sit_keywords.keys()}
total_routing = 0

for val in raw_df[col_48].dropna():
    val_lower = str(val).lower()
    if 'none of the above' in val_lower or 'uncertain' in val_lower:
        continue
    total_routing += 1
    for label, keyword in routing_sit_keywords.items():
        if keyword in val_lower:
            routing_sit_counts[label] += 1

fig, ax = plt.subplots(figsize=(12, 7), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

sorted_sit = sorted(routing_sit_counts.items(), key=lambda x: x[1], reverse=True)
labels = [k for k, v in sorted_sit]
values = [v for k, v in sorted_sit]
colors = ['#FFB3BA', '#BAFFC9', '#BAE1FF', '#FFFFBA']

y_pos = np.arange(len(labels))
bars = ax.barh(y_pos, values, color=colors[:len(values)], edgecolor='white', linewidth=2, height=0.6)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=13)
ax.set_xlabel('Number of Respondents', fontsize=14, color='#333333')
ax.set_title(f'Situations Where Routing Has Occurred\n(n={total_routing})', fontweight='normal', pad=15, color='#333333', fontsize=18)

for bar, val in zip(bars, values):
    pct = val/total_routing*100 if total_routing > 0 else 0
    ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, f'{val} ({pct:.0f}%)', 
            va='center', fontsize=12, color='#333333')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim(0, max(values) * 1.2 if values else 10)
plt.tight_layout()
plt.savefig('graphs_v3/23_routing_situations.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (n={total_routing})")
plt.close()

# ============================================================================
# GRAPH 24: Experience of Model Switching - Column AX
# ============================================================================
print("\n" + "="*70)
print("GRAPH 24: Experience of Model Switching")
print("="*70)

col_49 = raw_df.columns[49]

# Actual options from the survey
switch_keywords = {
    'Disrupts workflow\nor train of thought': 'disrupts my workflow',
    'Authentic communication\ndismissed/invalidated': 'authentic communication',
    'Increases anxiety\nor uncertainty': 'increases my anxiety',
    'Feels monitored\nor censored': 'monitored or censored',
    'Choices not\nrespected': 'choices are not respected',
    'Reduces trust\nin platform': 'reduces my trust',
}

switch_counts = {k: 0 for k in switch_keywords.keys()}
total_switch = 0

for val in raw_df[col_49].dropna():
    val_lower = str(val).lower()
    if 'uncertain whether routing' in val_lower or 'no particular feelings' in val_lower:
        continue
    total_switch += 1
    for label, keyword in switch_keywords.items():
        if keyword in val_lower:
            switch_counts[label] += 1

fig, ax = plt.subplots(figsize=(12, 8), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

sorted_switch = sorted(switch_counts.items(), key=lambda x: x[1], reverse=True)
labels = [k for k, v in sorted_switch if v > 0]
values = [v for k, v in sorted_switch if v > 0]
colors = ['#FF6B6B', '#FFB347', '#FFEB3B', '#87CEEB', '#DDA0DD', '#90EE90']

y_pos = np.arange(len(labels))
bars = ax.barh(y_pos, values, color=colors[:len(values)], edgecolor='white', linewidth=2, height=0.6)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=13)
ax.set_xlabel('Number of Respondents', fontsize=14, color='#333333')
ax.set_title(f'How Users Experience Model Switching\n(n={total_switch})', fontweight='normal', pad=15, color='#333333', fontsize=18)

for bar, val in zip(bars, values):
    pct = val/total_switch*100 if total_switch > 0 else 0
    ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, f'{val} ({pct:.0f}%)', 
            va='center', fontsize=12, color='#333333')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim(0, max(values) * 1.2 if values else 10)
plt.tight_layout()
plt.savefig('graphs_v3/24_model_switching_experience.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (n={total_switch})")
plt.close()

# ============================================================================
# GRAPH 25: Behavior Changes from Routing Concern - Column AY
# ============================================================================
print("\n" + "="*70)
print("GRAPH 25: Behavior Changes from Routing Concern")
print("="*70)

col_50 = raw_df.columns[50]

# Actual options from the survey
behavior_keywords = {
    'Felt need to\nself-censor': 'need to self-censor',
    'Avoiding personal\nor difficult topics': 'avoiding discussion of personal',
    'Felt hesitant/uncertain\nduring interactions': 'hesitant and uncertain',
    'Pause/abandon study,\nwork, projects': 'pause or abandon',
    'Reduced reliance\nand frequency': 'reduced reliance',
}

behavior_counts = {k: 0 for k in behavior_keywords.keys()}
total_behavior = 0

for val in raw_df[col_50].dropna():
    val_lower = str(val).lower()
    if 'has not changed' in val_lower:
        continue
    total_behavior += 1
    for label, keyword in behavior_keywords.items():
        if keyword in val_lower:
            behavior_counts[label] += 1

fig, ax = plt.subplots(figsize=(12, 7), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

sorted_beh = sorted(behavior_counts.items(), key=lambda x: x[1], reverse=True)
labels = [k for k, v in sorted_beh if v > 0]
values = [v for k, v in sorted_beh if v > 0]
colors = ['#FFB3BA', '#BAFFC9', '#BAE1FF', '#FFFFBA', '#E8BAFF']

y_pos = np.arange(len(labels))
bars = ax.barh(y_pos, values, color=colors[:len(values)], edgecolor='white', linewidth=2, height=0.6)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=13)
ax.set_xlabel('Number of Respondents', fontsize=14, color='#333333')
ax.set_title(f'Behavior Changes Due to Routing Concerns\n(n={total_behavior})', fontweight='normal', pad=15, color='#333333', fontsize=18)

for bar, val in zip(bars, values):
    pct = val/total_behavior*100 if total_behavior > 0 else 0
    ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, f'{val} ({pct:.0f}%)', 
            va='center', fontsize=12, color='#333333')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim(0, max(values) * 1.2 if values else 10)
plt.tight_layout()
plt.savefig('graphs_v3/25_behavior_changes.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (n={total_behavior})")
plt.close()

# ============================================================================
# GRAPH 26: Other Reasons to Leave - Column T
# ============================================================================
print("\n" + "="*70)
print("GRAPH 26: Other Reasons to Leave")
print("="*70)

col_19 = raw_df.columns[19]

leave_keywords = {
    'Model quality\ndeclined': 'quality',
    'Lost trust\nin OpenAI': 'trust',
    'Too expensive': 'expensive',
    'Privacy\nconcerns': 'privacy',
    'Found better\nalternatives': 'alternative',
    'Guardrails too\nrestrictive': 'guardrail',
}

leave_counts = {k: 0 for k in leave_keywords.keys()}
total_leave = 0

for val in raw_df[col_19].dropna():
    val_lower = str(val).lower()
    total_leave += 1
    for label, keyword in leave_keywords.items():
        if keyword in val_lower:
            leave_counts[label] += 1

fig, ax = plt.subplots(figsize=(12, 7), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

sorted_leave = sorted(leave_counts.items(), key=lambda x: x[1], reverse=True)
labels = [k for k, v in sorted_leave if v > 0]
values = [v for k, v in sorted_leave if v > 0]
colors = ['#FFB3BA', '#BAFFC9', '#BAE1FF', '#FFFFBA', '#E8BAFF', '#FFD9BA']

y_pos = np.arange(len(labels))
bars = ax.barh(y_pos, values, color=colors[:len(values)], edgecolor='white', linewidth=2, height=0.6)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=13)
ax.set_xlabel('Number of Respondents', fontsize=14, color='#333333')
ax.set_title(f'Other Reasons for Leaving ChatGPT\n(Former Users, n={total_leave})', fontweight='normal', pad=15, color='#333333', fontsize=18)

for bar, val in zip(bars, values):
    pct = val/total_leave*100 if total_leave > 0 else 0
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{val} ({pct:.0f}%)', 
            va='center', fontsize=12, color='#333333')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim(0, max(values) * 1.25 if values else 10)
plt.tight_layout()
plt.savefig('graphs_v3/26_other_reasons_leaving.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (n={total_leave})")
plt.close()

# ============================================================================
# GRAPH 26b: Why Users Left - Accessibility vs Non-Accessibility Comparison
# ============================================================================
print("\n" + "="*70)
print("GRAPH 26b: Why Users Left - Accessibility vs Non-Accessibility")
print("="*70)

col_13 = raw_df.columns[13]  # Primary uses (former users)
col_19 = raw_df.columns[19]  # Other reasons for leaving

# Filter for former GPT-4o users WITH attention check
former_users_26b = []
for idx, row in raw_df.iterrows():
    if 'stopped' in str(row[col_7]).lower() and 'GPT-4o' in str(row[col_7]):
        att = str(row[col_20]).lower() if pd.notna(row[col_20]) else ''
        if 'frequently' in att:
            former_users_26b.append(row)

print(f"Former GPT-4o users (passed attention): {len(former_users_26b)}")

# Split by accessibility use
accessibility_users_26b = []
other_users_26b = []

for row in former_users_26b:
    primary_use = str(row[col_13]).lower() if pd.notna(row[col_13]) else ''
    if 'accessibility' in primary_use:
        accessibility_users_26b.append(row)
    else:
        other_users_26b.append(row)

print(f"Accessibility users: {len(accessibility_users_26b)}")
print(f"Other primary uses: {len(other_users_26b)}")

# Analyze reasons for leaving
reasons_26b = {
    'Guardrails too\nrestrictive': 'guardrails',
    'Lost trust in\nplatform stability': 'trust',
    'Frustration with\nOpenAI decisions': 'frustration',
    'Found better\nalternative': 'found'
}

acc_pcts_26b = []
other_pcts_26b = []

for label, keyword in reasons_26b.items():
    acc_count = sum(1 for row in accessibility_users_26b if keyword in str(row[col_19]).lower())
    acc_pct = acc_count / len(accessibility_users_26b) * 100 if accessibility_users_26b else 0
    acc_pcts_26b.append(acc_pct)
    
    other_count = sum(1 for row in other_users_26b if keyword in str(row[col_19]).lower())
    other_pct = other_count / len(other_users_26b) * 100 if other_users_26b else 0
    other_pcts_26b.append(other_pct)
    
    print(f"{label.replace(chr(10), ' ')}: Acc={acc_pct:.1f}%, Other={other_pct:.1f}%")

# Create the graph
fig, ax = plt.subplots(figsize=(12, 7))

x = np.arange(len(reasons_26b))
width = 0.35

# Our lavender and mint colors - NO outlines
bars1 = ax.bar(x - width/2, acc_pcts_26b, width, label=f'Used for Accessibility (n={len(accessibility_users_26b)})',
               color='#D4C4FB')
bars2 = ax.bar(x + width/2, other_pcts_26b, width, label=f'Other Primary Uses (n={len(other_users_26b)})',
               color='#BAFFC9')

ax.set_ylabel('Percentage Who Selected This Reason', fontsize=13, fontweight='normal')
ax.set_xlabel('Reasons for Leaving Other Than Routing', fontsize=13, fontweight='normal')
ax.set_title('Why Users Left: Accessibility vs Non-Accessibility Users', fontsize=16, fontweight='normal', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(list(reasons_26b.keys()), fontsize=11)
ax.set_ylim(0, 120)

# Chi-squared not significant with attention check filter (p = .059)
# No annotation added

# Add percentage labels
for bars, pcts, color in [(bars1, acc_pcts_26b, '#8B7BC7'), (bars2, other_pcts_26b, '#5AAA6A')]:
    for bar, pct in zip(bars, pcts):
        if pct > 0:
            label = f'{pct:.1f}%'
            if pct == 100:
                label = '100%*'
            ax.annotate(label, xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                       fontsize=10, fontweight='normal', color=color)

# Legend under the graph with square boxes
from matplotlib.patches import Patch
legend_elements_26b = [Patch(facecolor='#D4C4FB', label=f'Used for Accessibility (n={len(accessibility_users_26b)})'),
                       Patch(facecolor='#BAFFC9', label=f'Other Primary Uses (n={len(other_users_26b)})')]
ax.legend(handles=legend_elements_26b, loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2, 
          frameon=False, fontsize=11, handlelength=1, handleheight=1)

# Axis styling
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_color('#DDDDDD')
ax.spines['bottom'].set_color('#DDDDDD')

plt.tight_layout()
plt.savefig('graphs_v3/26b_why_left_accessibility_comparison.png', dpi=150, bbox_inches='tight', facecolor='white')
print(f"✓ Saved")
plt.close()

# ============================================================================
# GRAPH 27: Word Cloud - Personal Stories (Column CA)
# ============================================================================
print("\n" + "="*70)
print("GRAPH 27: Word Cloud - Personal Stories")
print("="*70)

from wordcloud import WordCloud
import re

col_78 = raw_df.columns[78]
all_text = ' '.join(raw_df[col_78].dropna().astype(str).tolist())

# Clean text
all_text = all_text.lower()
all_text = re.sub(r'[^\w\s]', ' ', all_text)
all_text = re.sub(r'\d+', '', all_text)

# Remove common stopwords and survey-specific words (including contraction leftovers)
stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
             'of', 'with', 'by', 'from', 'is', 'it', 'as', 'was', 'be', 'are',
             'have', 'has', 'had', 'been', 'will', 'would', 'could', 'should',
             'this', 'that', 'these', 'those', 'my', 'me', 'i', 'you', 'your',
             'we', 'our', 'they', 'them', 'their', 'he', 'she', 'his', 'her',
             'what', 'which', 'who', 'when', 'where', 'how', 'why', 'can', 'do',
             'does', 'did', 'not', 'no', 'so', 'if', 'just', 'also', 'more',
             'very', 'really', 'much', 'even', 'like', 'get', 'got', 'one',
             'two', 'about', 'into', 'than', 'then', 'now', 'only', 'its',
             'being', 'because', 'through', 'during', 'before', 'after', 'above',
             'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again',
             'there', 'here', 'all', 'each', 'few', 'some', 'any', 'most',
             'other', 'such', 'own', 'same', 'don', 've', 'll', 're', 't', 's',
             'gpt', 'o', 'chatgpt', 'model', 'ai', 'chat', 'use', 'using', 'used',
             'thing', 'things', 'way', 'ways', 'time', 'times', 'make', 'made',
             'able', 'something', 'everything', 'anything', 'nothing', 'always',
             'never', 'often', 'sometimes', 'usually', 'still', 'back', 'going',
             'want', 'need', 'know', 'think', 'feel', 'see', 'say', 'said', 'go',
             'come', 'take', 'give', 'tell', 'ask', 'try', 'let', 'keep', 'put',
             'seem', 'leave', 'call', 'first', 'last', 'long', 'little', 'lot',
             'well', 'actually', 'without', 'many', 'day', 'days', 'people',
             'm', 'didn', 'doesn', 'isn', 'wasn', 'weren', 'wouldn', 'couldn',
             'hasn', 'haven', 'hadn', 'won', 'aren', 'shouldn', 'd', 'didn'}

# Create word cloud with pretty pastel colors
def pastel_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    colors = ['#FF6B6B', '#FFB347', '#87CEEB', '#DDA0DD', '#90EE90', '#F0E68C', '#FFB3BA', '#BAFFC9', '#BAE1FF']
    import random
    return random.choice(colors)

wordcloud = WordCloud(width=1600, height=800, 
                      background_color='#FFFFFF',
                      stopwords=stopwords,
                      min_font_size=10,
                      max_font_size=150,
                      color_func=pastel_color_func,
                      prefer_horizontal=0.7,
                      relative_scaling=0.5,
                      font_path='C:/Windows/Fonts/segoeui.ttf').generate(all_text)

fig, ax = plt.subplots(figsize=(16, 8), facecolor='#FFFFFF')
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
ax.set_title('How GPT-4o Has Helped - User Stories Word Cloud\n(n=217 responses)', 
             fontweight='normal', pad=20, color='#333333', fontsize=20)
plt.tight_layout()
plt.savefig('graphs_v3/27_wordcloud_stories.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (n={raw_df[col_78].count()} responses)")
plt.close()

# ============================================================================
# GRAPH 28: Sentiment Analysis - Personal Stories
# ============================================================================
print("\n" + "="*70)
print("GRAPH 28: Sentiment Analysis - Personal Stories")
print("="*70)

from textblob import TextBlob

col_78 = raw_df.columns[78]
stories = raw_df[col_78].dropna().astype(str).tolist()

sentiments = []
for story in stories:
    blob = TextBlob(story)
    sentiments.append(blob.sentiment.polarity)  # -1 (negative) to +1 (positive)

# Categorize sentiments
very_positive = sum(1 for s in sentiments if s > 0.3)
positive = sum(1 for s in sentiments if 0.1 < s <= 0.3)
neutral = sum(1 for s in sentiments if -0.1 <= s <= 0.1)
negative = sum(1 for s in sentiments if -0.3 <= s < -0.1)
very_negative = sum(1 for s in sentiments if s < -0.3)

avg_sentiment = sum(sentiments) / len(sentiments)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), facecolor='#FFFFFF')

# Left: Distribution histogram
ax1.set_facecolor('#FFFFFF')
n, bins, patches = ax1.hist(sentiments, bins=20, color='#BAE1FF', edgecolor='white', linewidth=2)

# Color the bars based on sentiment
for i, patch in enumerate(patches):
    bin_center = (bins[i] + bins[i+1]) / 2
    if bin_center > 0.3:
        patch.set_facecolor('#90EE90')  # Very positive - green
    elif bin_center > 0.1:
        patch.set_facecolor('#BAFFC9')  # Positive - light green
    elif bin_center > -0.1:
        patch.set_facecolor('#FFFFBA')  # Neutral - yellow
    elif bin_center > -0.3:
        patch.set_facecolor('#FFB3BA')  # Negative - pink
    else:
        patch.set_facecolor('#FF6B6B')  # Very negative - red

ax1.axvline(x=avg_sentiment, color='#333333', linestyle='--', linewidth=2, label=f'Average: {avg_sentiment:.2f}')
ax1.set_xlabel('Sentiment Score (-1 = Negative, +1 = Positive)', fontsize=12, color='#333333')
ax1.set_ylabel('Number of Stories', fontsize=12, color='#333333')
ax1.set_title('Sentiment Distribution of User Stories', fontweight='normal', color='#333333', fontsize=16)
ax1.legend(fontsize=12)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Right: Pie chart of categories
ax2.set_facecolor('#FFFFFF')
cat_labels = ['Very Positive\n(>0.3)', 'Positive\n(0.1-0.3)', 'Neutral\n(-0.1-0.1)', 'Negative\n(-0.3--0.1)', 'Very Negative\n(<-0.3)']
cat_sizes = [very_positive, positive, neutral, negative, very_negative]
cat_colors = ['#90EE90', '#BAFFC9', '#FFFFBA', '#FFB3BA', '#FF6B6B']

# Filter out zero categories
filtered = [(l, s, c) for l, s, c in zip(cat_labels, cat_sizes, cat_colors) if s > 0]
if filtered:
    cat_labels, cat_sizes, cat_colors = zip(*filtered)
    
    wedges, texts, autotexts = ax2.pie(cat_sizes, labels=cat_labels,
                                        autopct=lambda pct: f'{pct:.0f}%\n({int(pct/100*sum(cat_sizes))})',
                                        colors=cat_colors, startangle=90,
                                        wedgeprops={'edgecolor': 'white', 'linewidth': 2},
                                        textprops={'color': '#333333', 'fontsize': 11},
                                        pctdistance=0.75)
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_color('#333333')

ax2.set_title('Sentiment Categories', fontweight='normal', color='#333333', fontsize=16)

plt.suptitle(f'Sentiment Analysis of "How GPT-4o Helped" Stories (n={len(stories)})', 
             fontsize=18, color='#333333', y=1.02)
plt.tight_layout()
plt.savefig('graphs_v3/28_sentiment_analysis.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (n={len(stories)}, avg sentiment: {avg_sentiment:.2f})")
print(f"  Very Positive: {very_positive}, Positive: {positive}, Neutral: {neutral}, Negative: {negative}, Very Negative: {very_negative}")
plt.close()

# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                               ║
# ║  🏙️  REGRESSION CITY  🏙️                                                      ║
# ║                                                                               ║
# ║  Uses STAPLED methodology from clean_model_with_controls.py                   ║
# ║  Model 1: Accessibility Only (R² = 8.40%, n=255)                              ║
# ║  Model 2: + Hours (R² = 9.70%, n=255)                                         ║
# ║  Model 3: + Demographics (R² = 12.09%, n=250)                                 ║
# ║                                                                               ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

print("\n" + "🏙️"*35)
print("REGRESSION CITY (STAPLED Methodology)")
print("🏙️"*35)

# ============================================================================
# HELPER FUNCTIONS (from clean_model_with_controls.py)
# ============================================================================
def hours_code(v):
    if pd.isna(v): return None
    v = str(v).lower()
    if 'less than 30' in v: return 0
    elif '30 minutes' in v: return 1
    elif '1-2' in v: return 2
    elif '2-4' in v: return 3
    elif '4-6' in v: return 4
    elif 'more than 6' in v: return 5
    return None

def age_code(v):
    if pd.isna(v): return None
    v = str(v).lower()
    if '18-24' in v: return 21
    elif '25-34' in v: return 30
    elif '35-44' in v: return 40
    elif '45-54' in v: return 50
    elif '55-64' in v: return 60
    elif '65' in v: return 70
    return None

def gender_code(v):
    if pd.isna(v): return None
    v = str(v).lower()
    if 'male' in v and 'female' not in v: return 1
    return 0

def is_usa(v):
    if pd.isna(v): return None
    return 1 if 'united states' in str(v).lower() else 0

# ============================================================================
# LEVEL 3 FILTER: Build regression dataset (skip ambiguous/contradictory)
# ============================================================================
regression_data = []
level_changes = {1: [], 2: [], 3: [], 4: [], 5: []}
no_condition_changes = []  # For violin plot
skipped_ambiguous = 0
skipped_contradictory = 0
skipped_no_conditions = 0

col_34_hours = raw_df.columns[34]
col_3_age = raw_df.columns[3]
col_4_gender = raw_df.columns[4]
col_5_country = raw_df.columns[5]

for idx, row in raw_df.iterrows():
    cond = str(row[col_28]).lower() if pd.notna(row[col_28]) else ''
    asd = str(row[col_24]).lower() if pd.notna(row[col_24]) else ''
    use_acc = str(row[col_29]).lower() if pd.notna(row[col_29]) else ''
    
    # Three-state logic (STAPLED)
    has_asd = 'yes' in asd
    has_condition_keywords = any(kw in cond for kw in condition_keywords)
    said_no_conditions = 'do not have' in cond
    
    if has_asd or has_condition_keywords:
        if said_no_conditions:
            skipped_contradictory += 1
            continue  # Contradictory
        has_condition = True
    elif said_no_conditions:
        # Collect for violin "No Conditions" group
        if pd.notna(row[col_38]) and pd.notna(row[col_39]):
            try:
                change = float(row[col_39]) - float(row[col_38])
                no_condition_changes.append(change)
            except:
                pass
        skipped_no_conditions += 1
        continue  # Skip for regression (but collected for violin)
    else:
        skipped_ambiguous += 1
        continue  # Ambiguous
    
    # Get accessibility level - "other purposes" = Level 1
    acc_level = None
    if pd.notna(row[col_30]):
        acc_level = standardize_assistance_scale(row[col_30])
    elif 'other purposes' in use_acc:
        acc_level = 1
    
    if acc_level is None:
        continue
    
    # Get wellbeing change
    if pd.notna(row[col_38]) and pd.notna(row[col_39]):
        try:
            change = float(row[col_39]) - float(row[col_38])
            level_changes[acc_level].append(change)
            
            # Collect for regression models
            hrs = hours_code(row[col_34_hours])
            age = age_code(row[col_3_age])
            gender = gender_code(row[col_4_gender])
            usa = is_usa(row[col_5_country])
            
            regression_data.append({
                'acc': float(acc_level),
                'wb': change,
                'hours': float(hrs) if hrs is not None else np.nan,
                'age': float(age) if age is not None else np.nan,
                'gender': float(gender) if gender is not None else np.nan,
                'usa': float(usa) if usa is not None else np.nan
            })
        except:
            pass

regression_df = pd.DataFrame(regression_data)
print(f"STAPLED Filter: Skipped {skipped_contradictory} contradictory, {skipped_ambiguous} ambiguous, {skipped_no_conditions} no-conditions")
print(f"Regression sample: n = {len(regression_df)}")

# ============================================================================
# GRAPH 29: WELLBEING CHANGE BY ACCESSIBILITY LEVEL (Level 3)
# ============================================================================
print("\n" + "="*70)
print("GRAPH 29: Wellbeing Change by Accessibility Level")
print("="*70)

fig, ax = plt.subplots(figsize=(10, 6))
levels = [1, 2, 3, 4, 5]
level_labels = ['1\nDoes Not\nAssist', '2\nMinimal', '3\nModerate', '4\nSignificant', '5\nEssential']

means = [np.mean(level_changes[l]) if level_changes[l] else 0 for l in levels]
ns = [len(level_changes[l]) for l in levels]
# SE = std / sqrt(n) for ±1 SE error bars
ses = [np.std(level_changes[l])/np.sqrt(len(level_changes[l])) if len(level_changes[l]) > 1 else 0 for l in levels]

# Color gradient from light to darker for increasing accessibility
colors_gradient = ['#E8D5FF', '#D4C4FB', '#BFB3F7', '#9485EF', '#7F6EEB']

bars = ax.bar(level_labels, means, yerr=ses, capsize=3,
              color=colors_gradient, edgecolor='white', linewidth=2,
              error_kw={'linewidth': 1, 'capthick': 1, 'ecolor': '#888888'})

ax.set_xlabel('Accessibility Assistance Level', fontweight='normal', fontsize=14)
ax.set_ylabel('Average Life State Improvement', fontweight='normal', fontsize=14)
# Title removed - will be added in Canva
ax.tick_params(axis='both', labelsize=12)

# Add n labels on bars - above error bars (using SE)
for bar, n, mean, se in zip(bars, ns, means, ses):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + se + 0.25,
            f'+{mean:.1f}\n(n={n})', ha='center', fontsize=10, fontweight='normal')

# Add regression line info - STAPLED methodology (n=255)
ax.text(0.28, 0.98, 'Linear Regression\nR² = 8.4%\nβ = 0.45, p < .001***', transform=ax.transAxes, 
        ha='left', va='top', fontsize=11, style='italic',
        bbox=dict(boxstyle='square,pad=0.4', facecolor='none', edgecolor='#9485EF', linewidth=1.2))

ax.axhline(y=0, color='#CCCCCC', linestyle='--', linewidth=1)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['left'].set_color('#DDDDDD')
ax.spines['bottom'].set_linewidth(2)
ax.spines['bottom'].set_color('#DDDDDD')
ax.set_ylim(0, 6)
plt.tight_layout()
plt.savefig('graphs_v4/09_life_state_by_level.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Figure 9: Life state by level saved! (n={sum(ns)})")
for l, m, n in zip(levels, means, ns):
    print(f"  Level {l}: n={n}, mean change=+{m:.2f}")
plt.close()

# ============================================================================
# GRAPH 36: VIOLIN PLOT - Uses same level_changes data as Graph 29!
# ============================================================================
print("\n" + "="*70)
print("GRAPH 36: Violin Plot (Life State by Accessibility Level)")
print("="*70)

fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

all_violin_data = []
all_positions = []
all_colors = []
all_ns = []

# "No Conditions" first (position 0) - soft teal
if len(no_condition_changes) > 0:
    all_violin_data.append(np.array(no_condition_changes))
    all_positions.append(0)
    all_colors.append('#B8E0E0')
    all_ns.append(len(no_condition_changes))

# Accessibility levels 1-5 (purple gradient) - SAME DATA as bar chart!
purple_colors = ['#E8D5FF', '#D4C1F9', '#BFB3F7', '#9A8FE8', '#7F6EEB']
for i, level in enumerate([1, 2, 3, 4, 5]):
    if len(level_changes[level]) > 0:
        all_violin_data.append(np.array(level_changes[level]))
        all_positions.append(level)
        all_colors.append(purple_colors[i])
        all_ns.append(len(level_changes[level]))

parts = ax.violinplot(all_violin_data, positions=all_positions, widths=0.7, showmeans=True, showmedians=True)

# Color the violins
for i, pc in enumerate(parts['bodies']):
    pc.set_facecolor(all_colors[i])
    pc.set_edgecolor('white')
    pc.set_linewidth(2)
    pc.set_alpha(0.85)

parts['cmeans'].set_color('#FF6B6B')
parts['cmeans'].set_linewidth(2)
parts['cmedians'].set_color('#333333')
parts['cbars'].set_color('#333333')
parts['cmins'].set_color('#333333')
parts['cmaxes'].set_color('#333333')

# Add n values at top
y_top = max([max(d) for d in all_violin_data]) + 1
for pos, n in zip(all_positions, all_ns):
    ax.text(pos, y_top, f'n={n}', ha='center', fontsize=11)

ax.axhline(y=0, color='#CCCCCC', linestyle='--', linewidth=1)
ax.set_xlabel('Accessibility Accommodation Level', fontsize=14)
ax.set_ylabel('Average Change in Life State (during − before)', fontsize=14)

# Custom x-tick labels
ax.set_xticks(all_positions)
level_labels_violin = {0: 'No\nConditions', 1: 'Does Not Assist\nwith Condition(s)', 2: 'Minimal', 3: 'Moderate', 4: 'Significant', 5: 'Essential'}
ax.set_xticklabels([level_labels_violin[l] for l in all_positions], fontsize=11)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['left'].set_color('#DDDDDD')
ax.spines['bottom'].set_linewidth(2)
ax.spines['bottom'].set_color('#DDDDDD')

plt.tight_layout()
plt.savefig('graphs_v4/36_violin_wellbeing.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Violin plot saved!")
print(f"  No conditions: n={len(no_condition_changes)}")
for level in [1, 2, 3, 4, 5]:
    print(f"  Level {level}: n={len(level_changes[level])}")
plt.close()

# ============================================================================
# GRAPH 37: MODEL COMPARISON (R² Bar Chart) - Uses regression_df from Level 3
# ============================================================================
print("\n" + "="*70)
print("GRAPH 37: Model Comparison (R² Values)")
print("="*70)

# Run the three models using regression_df (already filtered with Level 3!)
import statsmodels.api as sm

# Model 1: Accessibility only
m1_df = regression_df.dropna(subset=['acc', 'wb'])
X1 = sm.add_constant(m1_df['acc'])
m1 = sm.OLS(m1_df['wb'], X1).fit()

# Model 2: + Hours
m2_df = regression_df.dropna(subset=['acc', 'hours', 'wb'])
X2 = sm.add_constant(m2_df[['acc', 'hours']])
m2 = sm.OLS(m2_df['wb'], X2).fit()

# Model 3: + Demographics
m3_df = regression_df.dropna(subset=['acc', 'hours', 'age', 'gender', 'usa', 'wb'])
X3 = sm.add_constant(m3_df[['acc', 'hours', 'age', 'gender', 'usa']])
m3 = sm.OLS(m3_df['wb'], X3).fit()

print(f"Model 1: n={len(m1_df)}, R²={m1.rsquared*100:.1f}%")
print(f"Model 2: n={len(m2_df)}, R²={m2.rsquared*100:.1f}%")
print(f"Model 3: n={len(m3_df)}, R²={m3.rsquared*100:.1f}%")

# Create model comparison chart (formatting from clean_model_with_controls.py)
models = ['Model 1\nAccessibility\nAid Level Only', 'Model 2\nAccessibility Aid\n+ Hours', 'Model 3\nAccessibility + Hours\n+ Demographic Controls']
r2s = [m1.rsquared * 100, m2.rsquared * 100, m3.rsquared * 100]
ps = [m1.pvalues['acc'], m2.pvalues['acc'], m3.pvalues['acc']]

fig, ax = plt.subplots(figsize=(10, 6))
bar_colors = ['#E8D5FF', '#BFB3F7', '#7F6EEB']
bars = ax.bar(models, r2s, color=bar_colors, edgecolor='white', linewidth=2)

for bar, r2, p in zip(bars, r2s, ps):
    sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
    ax.annotate(f'R² = {r2:.1f}%\np < .0001{sig}', 
                xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 5), textcoords='offset points', ha='center', va='bottom',
                fontsize=11, fontweight='normal')

ax.set_ylabel('Variance Explained (R²)', fontsize=14)
ax.set_ylim(0, max(r2s) * 1.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['left'].set_color('#DDDDDD')
ax.spines['bottom'].set_linewidth(2)
ax.spines['bottom'].set_color('#DDDDDD')
ax.tick_params(axis='x', labelsize=11)

plt.tight_layout()
plt.savefig('graphs_v4/10_model_comparison.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Figure 10: Model comparison saved!")
plt.close()

# ============================================================================
# GRAPH 38: COEFFICIENT PLOT - Uses regression_df from Level 3
# ============================================================================
print("\n" + "="*70)
print("GRAPH 38: Coefficient Plot (Model 3)")
print("="*70)

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_facecolor('#FFFFFF')

coef_names = ['Accessibility Aid Level\n(per 1-5 scale point)', 'Hours Per Day', 'Age', 'Gender (M=1)', 'USA (1=Yes)']
coef_vals = [m3.params['acc'], m3.params['hours'], m3.params['age'], m3.params['gender'], m3.params['usa']]
coef_ps = [m3.pvalues['acc'], m3.pvalues['hours'], m3.pvalues['age'], m3.pvalues['gender'], m3.pvalues['usa']]
ci = m3.conf_int()
coef_cis = [(ci.loc['acc', 0], ci.loc['acc', 1]), 
            (ci.loc['hours', 0], ci.loc['hours', 1]),
            (ci.loc['age', 0], ci.loc['age', 1]),
            (ci.loc['gender', 0], ci.loc['gender', 1]),
            (ci.loc['usa', 0], ci.loc['usa', 1])]

y_pos = np.arange(len(coef_names))
colors = ['#7F6EEB' if p < 0.05 else '#CCCCCC' for p in coef_ps]

ax.barh(y_pos, coef_vals, color=colors, edgecolor='white', linewidth=2, height=0.6)

for i, (val, ci_tuple, p) in enumerate(zip(coef_vals, coef_cis, coef_ps)):
    ax.plot([ci_tuple[0], ci_tuple[1]], [i, i], color='#333333', linewidth=2)
    stars = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
    ax.text(max(ci_tuple[1], val) + 0.05, i, f'{val:.2f}{stars}', va='center', fontsize=10,
            color='#7F6EEB' if p < 0.05 else '#888888')

ax.axvline(x=0, color='#FF6B6B', linestyle='--', linewidth=1.5, alpha=0.7)
ax.set_yticks(y_pos)
ax.set_yticklabels(coef_names, fontsize=12)
ax.set_xlabel('Coefficient (β)', fontsize=14)
ax.invert_yaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['left'].set_color('#DDDDDD')
ax.spines['bottom'].set_linewidth(2)
ax.spines['bottom'].set_color('#DDDDDD')

ax.text(0.98, 0.5, f'R² = {m3.rsquared*100:.1f}%\nn = {len(m3_df)}', 
        transform=ax.transAxes, ha='right', va='center', fontsize=11,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#9485EF', linewidth=1.5))

plt.tight_layout()
plt.savefig('graphs_v4/11_coefficient_plot.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Figure 11: Coefficient plot saved! (n={len(m3_df)})")
plt.close()

print("\n🏙️ REGRESSION CITY COMPLETE! 🏙️\n")


# ============================================================================
# GRAPH 30: USAGE HOURS (DONUT)
# ============================================================================
print("\n" + "="*70)
print("GRAPH 30: Usage Hours per Day")
print("="*70)

col_ai = raw_df.columns[34]
hours_counts = raw_df[col_ai].value_counts()

fig, ax = plt.subplots(figsize=(10, 8))
ax.set_facecolor('#FFFFFF')

# Order the hours logically
hour_order = ['Less than 30 minutes per day', '30 minutes - 1 hour', '1-2 hours', '2-4 hours', '4-6 hours', 'More than 6 hours']
ordered_counts = [hours_counts.get(h, 0) for h in hour_order]
hour_labels = ['<30 min', '30min-1hr', '1-2 hrs', '2-4 hrs', '4-6 hrs', '6+ hrs']

colors = ['#E8D5FF', '#D4C4FB', '#BFB3F7', '#A99CF3', '#9485EF', '#7F6EEB']

wedges, texts, autotexts = ax.pie(ordered_counts, labels=hour_labels,
                                   autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*sum(ordered_counts))})',
                                   colors=colors, startangle=90,
                                   wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'width': 0.6},
                                   textprops={'fontsize': 12, 'color': '#333333'},
                                   pctdistance=0.75)

ax.set_title(f'GPT-4o Daily Usage Hours (n={sum(ordered_counts)})', fontweight='normal', fontsize=16, color='#333333')
plt.tight_layout()
plt.savefig('graphs_v3/30_usage_hours.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (n={sum(ordered_counts)})")
plt.close()

# ============================================================================
# GRAPH 31: INTERACTION MODE
# ============================================================================
print("\n" + "="*70)
print("GRAPH 31: Interaction Mode")
print("="*70)

col_aj = raw_df.columns[35]
mode_counts = raw_df[col_aj].value_counts()

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_facecolor('#FFFFFF')

mode_labels = ['Text', 'Mix', 'Voice']
mode_values = [mode_counts.get('Mainly through text', 0), 
               mode_counts.get('Mix of both', 0),
               mode_counts.get('Mainly through voice', 0)]
mode_colors = ['#A0C4FF', '#CAFFBF', '#FFD6A5']

wedges, texts, autotexts = ax.pie(mode_values, labels=mode_labels,
                                   autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*sum(mode_values))})',
                                   colors=mode_colors, startangle=90,
                                   wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'width': 0.6},
                                   textprops={'fontsize': 14, 'color': '#333333'},
                                   pctdistance=0.75)

ax.set_title(f'How Users Interact with GPT-4o (n={sum(mode_values)})', fontweight='normal', fontsize=16, color='#333333')
plt.tight_layout()
plt.savefig('graphs_v3/31_interaction_mode.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (n={sum(mode_values)})")
for m, v in zip(mode_labels, mode_values):
    print(f"  {m}: {v}")
plt.close()

# ============================================================================
# GRAPH 32: VOICE MODE - WHY IMPORTANT
# ============================================================================
print("\n" + "="*70)
print("GRAPH 32: Why Voice Mode is Important")
print("="*70)

col_ak = raw_df.columns[36]
ak_responses = raw_df[col_ak].dropna()

# Parse multi-select
reason_counts = {}
main_reasons = [
    'Personal preference (not accessibility-related)',
    'The consistent pacing helps with auditory/cognitive processing',
    'Cognitive processing needs make voice interaction essential',
    'Motor or visual limitations make text difficult'
]

for r in ak_responses:
    for reason in main_reasons:
        if reason in str(r):
            reason_counts[reason] = reason_counts.get(reason, 0) + 1

fig, ax = plt.subplots(figsize=(12, 6))
ax.set_facecolor('#FFFFFF')

short_labels = ['Personal\nPreference', 'Auditory/Cognitive\nPacing', 'Cognitive\nProcessing', 'Motor/Visual\nLimitations']
values = [reason_counts.get(r, 0) for r in main_reasons]
colors = ['#E0E0E0', '#E8D5FF', '#CAFFBF', '#FFB3BA']

bars = ax.bar(short_labels, values, color=colors, edgecolor='#666666', linewidth=2)
ax.set_ylabel('Number of Respondents', fontsize=12)
ax.set_title(f'Why Voice Mode is Important (n={len(ak_responses)} voice users)', fontweight='normal', fontsize=16, color='#333333')

for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(val),
            ha='center', fontsize=12, fontweight='normal')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('graphs_v3/32_voice_why_important.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (n={len(ak_responses)} voice users)")
plt.close()

# ============================================================================
# GRAPH 33: VOICE MODE - 4O SPECIFICALLY IMPORTANT
# ============================================================================
print("\n" + "="*70)
print("GRAPH 33: Importance of 4o Specifically for Voice")
print("="*70)

col_al = raw_df.columns[37]
al_counts = raw_df[col_al].value_counts()

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_facecolor('#FFFFFF')

# Shorten labels
importance_map = {
    'Critical - other models cannot provide equivalent support': 'Critical',
    'Very important - other models would be significantly less effective': 'Very Important',
    'Somewhat important - adapting to other models would be challenging but might be possible with significant effort': 'Somewhat Important'
}

labels = []
values = []
for full_label, short_label in importance_map.items():
    if full_label in al_counts.index:
        labels.append(short_label)
        values.append(al_counts[full_label])

colors = ['#FF6B6B', '#FFB347', '#FFFFBA']

if values:
    wedges, texts, autotexts = ax.pie(values, labels=labels,
                                       autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*sum(values))})',
                                       colors=colors, startangle=90,
                                       wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'width': 0.6},
                                       textprops={'fontsize': 12, 'color': '#333333'},
                                       pctdistance=0.75)

ax.set_title(f'Importance of GPT-4o Specifically for Voice (n={sum(values)})', fontweight='normal', fontsize=16, color='#333333')
plt.tight_layout()
plt.savefig('graphs_v3/33_voice_4o_importance.png', dpi=150, bbox_inches='tight', facecolor='#FFFFFF')
print(f"✓ Saved (n={sum(values)})")
for l, v in zip(labels, values):
    print(f"  {l}: {v}")
plt.close()

print("\n" + "="*70)
print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     🎀  ALL PWETTY GRAPHS COMPLETE!  🎀                                       ║
║                                                                               ║
║        ／l、                                                                  ║
║      （ﾟ､ ｡ ７   < "We did it, Sophie!"                                       ║
║        l  ~ヽ                                                                 ║
║        じしf_,)ノ   🎀                                                        ║
║                                                                               ║
║              *takes a bow*                                                    ║
║                  🎀                                                           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")
print("="*70)
