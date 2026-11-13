#!/usr/bin/env python3
"""Build the Lain Kettu theme (lain.json) from the Midnight Vencord base.

Base = union of the two shipped copies of the same theme:
  - ThemeHub marketplace copy (themes/approved/midnight-vencord-1756294017700.json)
  - upstream discord-mobile-themes copy (midnight-vencord.json)
Union keeps every semanticColors/rawColors key either copy ships, so Discord
353.0 surfaces are covered whichever key set it reads. DMT wins on conflicts
(it is the properly-ramped upstream version).

Recolour: Lain palette — near-black blue-grey base, soft phosphor green,
lavender, warm beige/brown hair accent. NO neon/glow. Every key kept,
values only.
"""
import json, re, sys

HEX = re.compile(r'^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$')

# ---------------------------------------------------------------- palette
BG0 = '#0d1017'   # deepest (nav bar, backdrop)
BG1 = '#12161d'   # primary chat background
BG2 = '#161b25'   # secondary (sidebar)
BG3 = '#1b212e'   # tertiary
BG4 = '#202637'   # raised / floating / cards / inputs
BG5 = '#2a3040'   # selected / hovered controls
BORDER = '#2a3040'
BORDER_STRONG = '#3a4356'
TEXT = '#e9e6de'   # warm off-white
TEXT_MUT = '#9aa2b4'  # cool grey-lavender
TEXT_SUB = '#7c8496'
GREEN = '#7fb685'  # soft phosphor green (brand / accent)
GREEN_L = '#a9d3a6'
GREEN_D = '#548a5f'
LAV = '#a89cc8'    # lavender (links, secondary accent)
LAV_L = '#c3b8dc'
BEIGE = '#c8a97e'  # warm beige / Lain hair accent
BEIGE_D = '#a9885f'
ROSE = '#c07a7a'   # muted rose (danger / critical)
ROSE_D = '#965656'
GREY_MID = '#6f7688'

def a(hex6, alpha):
    """hex6 + 2-digit alpha suffix, e.g. a('#7fb685','33') -> '#7fb68533'."""
    return hex6 + alpha

# ------------------------------------------------------- raw colour ramps
# Each Discord ramp runs 260 (lightest) -> 700 (darkest). Lain equivalents
# keep the same lightness progression, family semantics preserved.
RAMPS = {
 'GREEN': {260:'#a9d3a6',300:'#9ccb97',330:'#8fc48a',345:'#83bc7e',360:'#7fb685',
           400:'#6fa878',430:'#639c6c',460:'#548a5f',500:'#47794f',530:'#3a6542',
           560:'#2f5236',600:'#263f2b',630:'#1b2e1f',660:'#142216',700:'#0c140d'},
 'BLUE':  {260:'#b3b8dc',300:'#a8aed6',330:'#9da4cf',345:'#9299c6',360:'#8790bd',
           400:'#767fb0',430:'#68719e',460:'#59618a',500:'#4a5175',530:'#3d4260',
           560:'#31354c',600:'#262a3b',630:'#1a1d2a',660:'#12141d',700:'#0a0b11'},
 'BRAND': {200:'#c4e0bd',260:'#a9d3a6',300:'#9ccb97',330:'#8fc48a',345:'#83bc7e',
           360:'#7fb685',400:'#6fa878',430:'#639c6c',460:'#548a5f',500:'#47794f',
           530:'#3a6542',560:'#2f5236',600:'#263f2b',630:'#1b2e1f',660:'#142216',
           700:'#0c140d',730:'#0a100b'},
 'TEAL':  {260:'#9db8a8',300:'#8fada0',330:'#82a296',345:'#75978c',360:'#6a8c81',
           400:'#5d7d73',430:'#526e65',460:'#465f57',500:'#3a4f48',530:'#30413b',
           560:'#26342f',600:'#1d2825',630:'#141c19',660:'#0e1412',700:'#080b0a'},
 'YELLOW':{260:'#e3cba3',300:'#dcc19c',330:'#d5b78f',345:'#cdae84',360:'#c8a97e',
           400:'#b7956a',430:'#a9885f',460:'#967752',500:'#836646',530:'#6d553b',
           560:'#57452f',600:'#423423',630:'#2d2418',660:'#1e1810',700:'#100d08'},
 'ORANGE':{260:'#d9b18c',300:'#d2a37c',330:'#c9966c',345:'#bf8a5f',360:'#b57e52',
           400:'#a06f47',430:'#8d613d',460:'#795234',500:'#66442c',530:'#543724',
           560:'#422c1d',600:'#302015',630:'#20150e',660:'#150e09',700:'#0b0704'},
 'RED':   {260:'#d8a0a0',300:'#d09393',330:'#c88787',345:'#c07a7a',360:'#b56e6e',
           400:'#a86262',430:'#965656',460:'#844a4a',500:'#723f3f',530:'#5e3434',
           560:'#4a2929',600:'#371e1e',630:'#261414',660:'#190d0d',700:'#0d0707'},
 'PINK':  {260:'#dccfe8',300:'#cdbfdd',330:'#bfafd2',345:'#b19fc7',360:'#a89cc8',
           400:'#9688b5',430:'#8576a3',460:'#746491',500:'#63547e',530:'#51446a',
           560:'#403555',600:'#302741',630:'#201a2c',660:'#15111d',700:'#0b090f'},
}
# PLUM / PRIMARY are the neutral scales in the gruvbox base; map by key to
# the blue-grey scale (lightest -> text, darkest -> deepest background).
PLUM_MAP = {
 'PLUM_1':'#e9e6de','PLUM_3':'#9aa2b4','PLUM_4':'#b3b8c4','PLUM_6':'#c9cdd6',
 'PLUM_9':'#9aa2b4','PLUM_10':'#6f7688','PLUM_11':'#5d6373','PLUM_12':'#2a3040',
 'PLUM_13':'#202637','PLUM_14':'#12161e','PLUM_15':'#2a3040','PLUM_16':'#202637',
 'PLUM_17':'#161b25','PLUM_18':'#1b212e','PLUM_19':'#12161e','PLUM_20':'#161b25',
 'PLUM_21':'#1b212e','PLUM_22':'#202637','PLUM_23':'#2a3040','PLUM_24':'#202637',
 'PLUM_25':'#161b25',
}
PRIMARY_MAP = {
 'PRIMARY_100':'#f2efe8','PRIMARY_130':'#e9e6de','PRIMARY_160':'#d5d2ca',
 'PRIMARY_200':'#c9cdd6','PRIMARY_230':'#b3b8c4','PRIMARY_300':'#9aa2b4',
 'PRIMARY_330':'#9aa2b4','PRIMARY_360':'#7c8496','PRIMARY_400':'#6f7688',
 'PRIMARY_430':'#6f7688','PRIMARY_460':'#3a4152','PRIMARY_500':'#2a3040',
 'PRIMARY_530':'#2a3040','PRIMARY_560':'#202637','PRIMARY_600':'#202637',
 'PRIMARY_630':'#161b25','PRIMARY_645':'#1b212e','PRIMARY_660':'#161b25',
 'PRIMARY_700':'#12161e','PRIMARY_730':'#9aa2b4','PRIMARY_800':'#11151d',
 'PRIMARY_830':'#11151d','PRIMARY_860':'#0d1017','PRIMARY_900':'#0d1017',
}
RED_NEW_MAP = {1:'#f2e3e3',10:'#e9d2d2',20:'#dfc0c0',30:'#d5aeae',40:'#cb9c9c',50:'#c07a7a'}
MISC_RAW = {
 'BLACK_500': '#000000b2',          # scrim black, keep (alpha included)
 'WHITE_500': '#ffffff',
 'WHITE_630': '#9aa2b4',
 'OPACITY_12': '#6f7688',
 'OPACITY_RED_4':  '#c07a7a0a', 'OPACITY_RED_8':  '#c07a7a14',
 'OPACITY_RED_12': '#c07a7a1f', 'OPACITY_RED_16': '#c07a7a29',
 'OPACITY_RED_20': '#c07a7a33',
 'GUILD_BOOSTING_PINK': '#a89cc8',
 'GUILD_BOOSTING_PURPLE': '#8a7cab',
 'GUILD_BOOSTING_PURPLE_FOR_GRADIENTS': '#a89cc8',
 'BLURPLE_50': '#a9d3a6', 'BLURPLE_65': '#8fc48a',
 'ROLE_DEFAULT': '#9aa2b4',
}

def remap_raw(key, value):
    """Return the Lain value for a rawColors entry, preserving any alpha."""
    alpha = ''
    v = value
    if isinstance(v, str) and len(v) == 9 and v.startswith('#'):
        alpha, v = v[7:], v[:7]
    m = re.match(r'^([A-Z_]+?)_?(\d+)?$', key)
    fam, num = m.group(1), m.group(2)
    if key in MISC_RAW:
        return MISC_RAW[key]
    if fam == 'PLUM' and key in PLUM_MAP:
        return PLUM_MAP[key] + alpha
    if fam == 'PRIMARY' and key in PRIMARY_MAP:
        return PRIMARY_MAP[key] + alpha
    if fam == 'RED' and num and key.startswith('RED_NEW'):
        return RED_NEW_MAP[int(num)] + alpha
    if fam in RAMPS and num and int(num) in RAMPS[fam]:
        return RAMPS[fam][int(num)] + alpha
    # last resort: map by lightness of the original value onto the bg scale
    return fallback_neutral(v) + alpha

def _lum(hex6):
    r, g, b = (int(hex6[i:i+2], 16) for i in (1, 3, 5))
    return (0.299*r + 0.587*g + 0.114*b) / 255

def fallback_neutral(hex6):
    l = _lum(hex6)
    if l > 0.85: return '#e9e6de'
    if l > 0.65: return '#c9cdd6'
    if l > 0.5:  return '#9aa2b4'
    if l > 0.38: return '#7c8496'
    if l > 0.28: return '#6f7688'
    if l > 0.2:  return '#3a4152'
    if l > 0.14: return '#2a3040'
    if l > 0.09: return '#202637'
    if l > 0.05: return '#161b25'
    return '#12161e'

# ---------------------------------------------------------- semantic map
# Exact overrides by key. Values are single hex strings; the builder wraps
# them back into the original container shape (list or plain string).
SEM = {
 # --- backgrounds ---
 'BACKGROUND_PRIMARY': BG1, 'CHAT_BACKGROUND': BG1, 'BG_BASE_PRIMARY': BG1,
 'BACKGROUND_BASE_LOWEST': BG1, 'HOME_BACKGROUND': BG1, 'MODAL_BACKGROUND': BG1,
 'PANEL_BG': BG1, 'CHANNEL_BACKGROUND_DEFAULT': BG1,
 'BACKGROUND_MOBILE_PRIMARY': BG1, 'MOBILE_CHATINPUT_BACKGROUND_DEFAULT': BG1,
 'MOBILE_CHATINPUT_BACKGROUND_ACTIVE': BG1, 'MOBILE_SEARCHBAR_GRADIENT_BACKGROUND': BG1,
 'BACKGROUND_MOBILE_SECONDARY': BG2,
 'CARD_PRIMARY_BG': BG4,
 'REDESIGN_CHANNEL_CATEGORY_NAME_TEXT': TEXT_MUT,
 'BORDER_FAINT': '#2a304033',
 'BACKGROUND_SECONDARY': BG2, 'BG_BASE_SECONDARY': BG2,
 'BACKGROUND_BASE_LOWER': BG2, 'BACKGROUND_BASE_LOW': BG2,
 'BACKGROUND_SECONDARY_ALT': BG2, 'MOBILE_ACTIONSHEET_BACKGROUND': BG2,
 'MOBILE_GUILDBAR_ICON_BACKGROUND_DEFAULT': BG2, 'KEYBOARD': BG2,
 'BACKGROUND_TERTIARY': BG3, 'BG_BASE_TERTIARY': BG3,
 'BACKGROUND_SURFACE_HIGH': BG3, 'BG_SURFACE_RAISED': BG3,
 'MODAL_FOOTER_BACKGROUND': BG0, 'MOBILE_FLOATINGBAR_BACKGROUND_SCRIM': BG0,
 'BACKGROUND_FLOATING': BG4, 'BACKGROUND_NESTED_FLOATING': BG4,
 'CARD_BACKGROUND_DEFAULT': BG4, 'CARD_SECONDARY_BACKGROUND_DEFAULT': BG4,
 'CARD_SECONDARY_BG': BG4, 'CARD_MUTED_BG': BG4, 'EMBED_BACKGROUND': BG4,
 'MOBILE_EMBED_BACKGROUND_DEFAULT': BG4, 'MOBILE_FLOATINGBAR_BACKGROUND': BG4,
 'MOBILE_FLOATINGBAR_BACKGROUND_NAMEPLATE': BG4,
 'MOBILE_FLOATING_ACCESSORY_BACKGROUND': BG4,
 'CHANNELTEXTAREA_BACKGROUND': BG4, 'CHAT_INPUT_BACKGROUND': BG4,
 'REDESIGN_CHAT_INPUT_BACKGROUND': BG4, 'INPUT_BACKGROUND_DEFAULT': BG4,
 'BACKGROUND_CODE': BG4, 'SPOILER_REVEALED_BACKGROUND': BG1,
 'SPOILER_HIDDEN_BACKGROUND': BG4, 'POLLS_NORMAL_IMAGE_BACKGROUND': BG4,
 'BACKGROUND_ACCENT': GREEN, 'BACKGROUND_BRAND': GREEN,
 'BACKGROUND_SCRIM': '#00000080', 'BG_BACKDROP': BG0,
 'BG_MOD_FAINT': '#e9e6de0f',
 'BACKGROUND_FEEDBACK_CRITICAL': '#c07a7a14',
 'BACKGROUND_MODIFIER_ACCENT': '#7fb6851f',
 'BACKGROUND_MODIFIER_ACCEPT': '#7fb68533',
 'BACKGROUND_MODIFIER_ACCEPT_HOVER': '#7fb68540',
 'BACKGROUND_MODIFIER_ACTIVE': '#e9e6de14',
 'BACKGROUND_MODIFIER_HOVER': '#e9e6de0d',
 'BACKGROUND_MODIFIER_SELECTED': '#e9e6de14',
 'BACKGROUND_MESSAGE_HOVER': '#e9e6de0a',
 'BACKGROUND_MENTIONED': '#7fb6851a', 'BACKGROUND_MENTIONED_HOVER': '#7fb68526',
 'MENTION_BACKGROUND': '#7fb68526', 'MENTION_FOREGROUND': GREEN_L,
 'THEME_LOCKED_BLUR_FALLBACK': '#12161df2',
 'ANDROID_NAVIGATION_BAR_BACKGROUND': BG0, 'ANDROID_RIPPLE': GREEN,
 'AUTOMOD_QUEUED_FOR_REVIEW_BACKGROUND': '#c8a97e14',
 'AUTOMOD_QUEUED_FOR_REVIEW_BACKGROUND_HOVER': '#c8a97e26',
 # --- text ---
 'TEXT_NORMAL': TEXT, 'TEXT_PRIMARY': TEXT, 'TEXT_DEFAULT': TEXT,
 'TEXT_STRONG': TEXT, 'HEADER_PRIMARY': TEXT,
 'REDESIGN_CHANNEL_NAME_TEXT': TEXT, 'MOBILE_TEXT_HEADING_PRIMARY': TEXT,
 'NAVIGATOR_HEADER_TINT': TEXT, 'INTERACTIVE_TEXT_ACTIVE': TEXT,
 'INTERACTIVE_ACTIVE': TEXT, 'CONTROL_SECONDARY_TEXT_DEFAULT': TEXT,
 'TEXT_SECONDARY': TEXT_MUT, 'HEADER_SECONDARY': TEXT_MUT,
 'TEXT_MUTED': TEXT_MUT, 'TEXT_SUBTLE': TEXT_MUT,
 'CHANNELS_DEFAULT': TEXT_MUT, 'CHANNEL_ICON': TEXT_MUT,
 'INTERACTIVE_NORMAL': TEXT_MUT, 'INTERACTIVE_MUTED': '#9aa2b466',
 'INTERACTIVE_TEXT_DEFAULT': TEXT_MUT, 'INTERACTIVE_ICON_DEFAULT': TEXT_MUT,
 'REDESIGN_CHANNEL_NAME_MUTED_TEXT': TEXT_MUT,
 'REDESIGN_BUTTON_TERTIARY_TEXT': TEXT_MUT, 'REACTION_TEXT_DEFAULT': TEXT_MUT,
 'MOBILE_GUILDBAR_ICON_DEFAULT': TEXT_MUT, 'INTERACTIVE_HOVER': '#c9cdd6',
 'TEXT_BRAND': LAV, 'TEXT_LINK': LAV,
 'TEXT_FEEDBACK_CRITICAL': ROSE,
 'CONTROL_PRIMARY_TEXT_DEFAULT': BG0, 'CONTROL_CRITICAL_PRIMARY_TEXT_DEFAULT': BG0,
 'CONTROL_EXPRESSIVE_TEXT_DEFAULT': BG0, 'CONTROL_CRITICAL_SECONDARY_TEXT_DEFAULT': ROSE,
 'REACTION_TEXT_REACTED_DEFAULT': GREEN_L,
 # --- brand / interactive green ---
 'CONTROL_BRAND_FOREGROUND': GREEN,
 'CONTROL_CONNECTED_BACKGROUND_DEFAULT': GREEN,
 'CONTROL_EXPRESSIVE_BACKGROUND_DEFAULT': GREEN,
 'CONTROL_PRIMARY_BACKGROUND_DEFAULT': GREEN,
 'REDESIGN_INPUT_CONTROL_SELECTED': GREEN, 'SPINE_DEFAULT': GREEN,
 'SWITCH_BACKGROUND_SELECTED_DEFAULT': GREEN,
 'SWITCH_BORDER_SELECTED_DEFAULT': GREEN,
 'REACTION_BACKGROUND_REACTED_DEFAULT': GREEN,
 'REACTION_BORDER_REACTED_DEFAULT': GREEN,
 'POLLS_VOTED_FILL': '#7fb68580', 'POLLS_VICTOR_FILL': '#7fb68580',
 'MOBILE_VOICE_MESSAGE_RECORDING_WAVEFORM_BAR_BACKGROUND': GREEN,
 'MOBILE_CHATINPUT_BORDER_ACTIVE': GREEN, 'BORDER_FOCUS': GREEN,
 'APP_FRAME_BORDER': BORDER_STRONG, 'POLLS_NORMAL_FILL_HOVER': '#7fb68526',
 # --- danger / critical rose ---
 'STATUS_DANGER': ROSE, 'STATUS_DANGER_BACKGROUND': ROSE,
 'STATUS_DANGER_TEXT': ROSE, 'ICON_FEEDBACK_CRITICAL': ROSE,
 'TEXT_FEEDBACK_CRITICAL': ROSE,
 'CONTROL_CRITICAL_PRIMARY_BACKGROUND_DEFAULT': ROSE,
 'CONTROL_CRITICAL_SECONDARY_BACKGROUND_DEFAULT': BG4,
 'REDESIGN_BUTTON_DANGER_BACKGROUND': ROSE,
 'BORDER_FEEDBACK_CRITICAL': '#c07a7a33',
 # --- borders ---
 'BORDER_STRONG': '#3a435655', 'BORDER_SUBTLE': '#2a304040',
 'CARD_BORDER_DEFAULT': BORDER, 'MOBILE_FLOATING_ACCESSORY_BORDER': BORDER,
 'MOBILE_CHATINPUT_BORDER_DEFAULT': BORDER,
 'REDESIGN_BUTTON_SECONDARY_BORDER': BORDER,
 # --- secondary controls ---
 'CONTROL_SECONDARY_BACKGROUND_DEFAULT': BG5,
 'REDESIGN_BUTTON_SECONDARY_BACKGROUND': BG5,
 'REDESIGN_BUTTON_SECONDARY_ALT_BACKGROUND': BG5,
 'REDESIGN_BUTTON_TERTIARY_BACKGROUND': BG5,
 'MOBILE_EMOJI_BUTTON_BACKGROUND': BG5,
 'MOBILE_CHANNEL_ITEM_BACKGROUND_SELECTED': BG5,
 'SLIDER_TRACK_BACKGROUND': BG5, 'SWITCH_BACKGROUND_DEFAULT': GREY_MID,
 'REACTION_BACKGROUND_DEFAULT': BG5, 'REACTION_BORDER_DEFAULT': GREY_MID,
 'SWITCH_BORDER_DEFAULT': GREY_MID,
 # --- misc ---
 'SCROLLBAR_AUTO_THUMB': BORDER_STRONG, 'SCROLLBAR_THIN_THUMB': BORDER_STRONG,
 'SCROLLBAR_AUTO_TRACK': BG1, 'SCROLLBAR_THIN_TRACK': BG1,
 'REDESIGN_ACTIVITY_CARD_BACKGROUND': BG4,
 'REDESIGN_ACTIVITY_CARD_BACKGROUND_PRESSED': BG3,
}

def remap_semantic(key, value):
    """value: list like ['#rrggbb'] or plain string. Returns same shape."""
    if key in SEM:
        new = SEM[key]
    else:
        # Fallback: keep semantics by key name, map old colour by family.
        raw = value[0] if isinstance(value, list) else value
        # NB: 'RED' must be a standalone token — 'REDESIGN' keys are not red.
        is_red = ('DANGER' in key or 'CRITICAL' in key or key.startswith('RED_')
                  or '_RED_' in key or key.endswith('_RED'))
        if is_red:
            new = ROSE
        elif 'BRAND' in key or 'ACCENT' in key or 'GREEN' in key:
            new = GREEN
        elif 'BACKGROUND' in key or 'BG_' in key or 'CARD' in key or 'MODAL' in key:
            new = fallback_neutral(raw)
        elif 'TEXT' in key or 'HEADER' in key or 'CHANNEL' in key or 'INTERACTIVE' in key:
            new = TEXT if _lum(raw) > 0.5 else TEXT_MUT
        elif 'BORDER' in key:
            new = BORDER
        else:
            new = fallback_neutral(raw)
        print(f'  [fallback] semantic {key}: {raw} -> {new}', file=sys.stderr)
    if isinstance(value, list):
        return [new]
    return new

def main():
    dmt = json.load(open('midnight-vencord-dmt.json'))
    mkt = json.load(open('midnight-vencord-raw.json'))
    sem, raw = {}, {}
    # union, DMT wins on conflicts
    for src in (mkt, dmt):
        sem.update(src.get('semanticColors', {}))
        raw.update(src.get('rawColors', {}))
    print(f'base union: {len(sem)} semantic, {len(raw)} raw', file=sys.stderr)

    new_sem = {k: remap_semantic(k, v) for k, v in sem.items()}
    new_raw = {k: remap_raw(k, v) for k, v in raw.items()}

    # validate every colour value is a valid hex (#rrggbb or #rrggbbaa)
    bad = []
    for k, v in new_sem.items():
        vals = v if isinstance(v, list) else [v]
        for x in vals:
            if not isinstance(x, str) or not HEX.match(x):
                bad.append(('semantic', k, x))
    for k, v in new_raw.items():
        if not isinstance(v, str) or not HEX.match(v):
            bad.append(('raw', k, v))
    if bad:
        print('INVALID VALUES:', bad, file=sys.stderr)
        sys.exit(1)

    out = {
        'id': 'lain-kettu-max',
        'filename': 'lain.json',
        'name': 'Lain — Serial Experiments Lain',
        'description': 'Serial Experiments Lain theme for Kettu (Discord iOS). Near-black blue-grey base, soft phosphor green, lavender, warm beige hair accent. Based on Midnight Vencord by refact0r.',
        'version': '1',
        'authors': [{'name': 'dolanexeee'}],
        'spec': 2,
        'previewUrl': 'https://dolanexeee.github.io/kettu-max/lain-preview.png',
        'repositoryUrl': 'https://github.com/dolanexeee/kettu-max',
        'source': 'local',
        'semanticColors': new_sem,
        'rawColors': new_raw,
        'plus': {
            'version': 0,
            'iconPack': 'rosiecord-plumpy',
            'mentionLineColor': GREEN,
            'customOverlays': True,
            'icons': {
                'trash': ROSE, 'TrashIcon': ROSE,
                'TriangleExclamationPointIcon': BEIGE,
                'toast_copy_link': GREEN_L,
                'toast_copy_message': TEXT, 'toast_image_saved': TEXT,
            },
        },
    }
    json.dump(out, open('lain.json', 'w'), indent=2, ensure_ascii=False)
    print(f'wrote lain.json: {len(new_sem)} semantic, {len(new_raw)} raw, 0 invalid', file=sys.stderr)

if __name__ == '__main__':
    main()
