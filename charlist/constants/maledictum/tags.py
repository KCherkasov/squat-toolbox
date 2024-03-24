# -*- coding: utf-8 -*-

ST_WEAPON_SKILL = 'ST_WS'
ST_BALLISTIC_SKILL = 'ST_BS'
ST_STRENGTH = 'ST_STR'
ST_TOUGHNESS = 'ST_T'
ST_AGILITY = 'ST_AG'
ST_INTELLIGENCE = 'ST_INT'
ST_PERCEPTION = 'ST_PER'
ST_WILLPOWER = 'ST_WP'
ST_FELLOWSHIP = 'ST_FEL'


STAT_TAGS = [ST_WEAPON_SKILL, ST_INTELLIGENCE, ST_BALLISTIC_SKILL,
             ST_PERCEPTION, ST_STRENGTH, ST_WILLPOWER,
             ST_TOUGHNESS, ST_FELLOWSHIP, ST_AGILITY]

STAT_TAGS_GEN = [ST_WEAPON_SKILL, ST_BALLISTIC_SKILL, ST_STRENGTH,
                 ST_TOUGHNESS, ST_AGILITY, ST_INTELLIGENCE,
                 ST_PERCEPTION, ST_WILLPOWER, ST_FELLOWSHIP]

SK_ATHLETICS = 'SK_ATHL'
SK_AWARENESS = 'SK_AWR'
SK_DEXTERITY = 'SK_DEX'
SK_DISCIPLINE = 'SK_DIS'
SK_FORTITUDE = 'SK_FORT'
SK_INTUITION = 'SK_INT'
SK_LINGUISTICS = 'SK_LNG'
SK_LOGIC = 'SK_LOG'
SK_LORE = 'SK_LORE'
SK_MEDICAE = 'SK_MED'
SK_MELEE = 'SK_MELEE'
SK_NAVIGATION = 'SK_NAV'
SK_PILOTING = 'SK_PILOT'
SK_PRESENCE = 'SK_PRES'
SK_PSYCHIC = 'SK_PSY'
SK_RANGED = 'SK_RNG'
SK_RAPPORT = 'SK_RAP'
SK_REFLEXES = 'SK_RFL'
SK_STEALTH = 'SK_STL'
SK_TECH = 'SK_TECH'

SKILL_TAGS = [SK_ATHLETICS, SK_AWARENESS, SK_DEXTERITY,  SK_DISCIPLINE, SK_FORTITUDE,  SK_INTUITION, SK_LINGUISTICS,
              SK_LOGIC,     SK_LORE,      SK_MEDICAE,    SK_MELEE,      SK_NAVIGATION, SK_PILOTING,  SK_PRESENCE,
              SK_PSYCHIC,   SK_RANGED,    SK_RAPPORT,    SK_REFLEXES,   SK_STEALTH,    SK_TECH]

SP_CLIMBING = 'SP_CLM'
SP_MIGHT = 'SP_MGT'
SP_RIDING = 'SP_RID'
SP_RUNNING = 'SP_RUN'
SP_SWIMMING = 'SP_SWM'
SP_HEARING = 'SP_HRN'
SP_SIGHT = 'SP_SGT'
SP_SMELL = 'SP_SML'
SP_TASTE = 'SP_TST'
SP_TOUCH = 'SP_TCH'
SP_PSYNISCIENCE = 'SP_AWR_PSY'
SP_LOCKPICKING = 'SP_LPK'
SP_PICKPOCKET = 'SP_PPKT'
SP_SLEIGHT_OF_HANDS = 'SP_SOH'
SP_DEFUSE = 'SP_DFS'
SP_COMPOSURE = 'SP_CMP'
SP_FEAR = 'SP_FEAR'
SP_PSYCHIC = 'SP_DSC_PSY'
SP_ENDURANCE = 'SP_END'
SP_PAIN = 'SP_PAIN'
SP_POISON = 'SP_PSN'
SP_PEOPLE = 'SP_PPL'
SP_SURROUNDINGS = 'SP_SRN'
SP_CIPHERS = 'SP_CPR'
SP_HIGH_GOTHIC = 'SP_HGT'
SP_EVALUATION = 'SP_EVL'
SP_INVESTIGATION = 'SP_INV'
SP_ACADEMICS = 'SP_ACDM'
SP_ADEPTUS_TERRA = 'SP_ADTR'
SP_SECTOR = 'SP_SCT'
SP_THEOLOGY = 'SP_THLG'
SP_MED_ANIMAL = 'SP_MED_ANM'
SP_HUMAN = 'SP_HMN'
SP_BRAWLING = 'SP_BRWL'
SP_ONE_HANDED = 'SP_OHD'
SP_TWO_HANDED = 'SP_THD'
SP_SURFACE = 'SP_SRF'
SP_TRACKING = 'SP_TRK'
SP_NAV_VOID = 'SP_VOID'
SP_NAV_WARP = 'SP_WRP'
SP_AERONAUTICA = 'SP_AER'
SP_CIVILIAN = 'SP_CIV'
SP_MILITARY = 'SP_MIL'
SP_MINOR_VOIDSHIP = 'SP_MNR_VDS'
SP_MAJOR_VOIDSHIP = 'SP_MJR_VDS'
SP_INTERROGATION = 'SP_INTRG'
SP_INTIMIDATION = 'SP_INTM'
SP_LEADERSHIP = 'SP_LDR'
SP_LONG_GUNS = 'SP_LNGN'
SP_ORNDANCE = 'SP_ORDN'
SP_PISTOLS = 'SP_PST'
SP_THROWN = 'SP_THR'
SP_RAP_ANIMALS = 'SP_RAP_ANML'
SP_CHARM = 'SP_CHR'
SP_DECEPTION = 'SP_DCP'
SP_HAGGLE = 'SP_HGL'
SP_INQUIRY = 'SP_INQ'
SP_ACROBATICS = 'SP_ACR'
SP_BALANCE = 'SP_BLN'
SP_DODGE = 'SP_DDG'
SP_CONCEAL = 'SP_CNCL'
SP_HIDE = 'SP_HIDE'
SP_MOVE_SILENTLY = 'SP_MVSL'
SP_AUGMETICS = 'SP_AUG'
SP_ENGINEERING = 'SP_ENG'
SP_SECURITY = 'SP_SEC'
SP_INHERIT = 'SP_INHERIT'

SKILL_SPECS = [SP_CLIMBING,      SP_MIGHT,         SP_RIDING,         SP_RUNNING,          SP_SWIMMING,
               SP_HEARING,       SP_SIGHT,         SP_SMELL,          SP_TASTE,            SP_TOUCH,
               SP_PSYNISCIENCE,  SP_LOCKPICKING,   SP_PICKPOCKET,     SP_SLEIGHT_OF_HANDS, SP_DEFUSE,
               SP_COMPOSURE,     SP_FEAR,          SP_PSYCHIC,        SP_ENDURANCE,        SP_POISON,
               SP_PEOPLE,        SP_SURROUNDINGS,  SP_CIPHERS,        SP_HIGH_GOTHIC,      SP_EVALUATION,
               SP_INVESTIGATION, SP_ACADEMICS,     SP_ADEPTUS_TERRA,  SP_SECTOR,           SP_THEOLOGY,
               SP_MED_ANIMAL,    SP_HUMAN,         SP_BRAWLING,       SP_ONE_HANDED,       SP_TWO_HANDED,
               SP_SURFACE,       SP_TRACKING,      SP_NAV_VOID,       SP_NAV_WARP,         SP_AERONAUTICA,
               SP_CIVILIAN,      SP_MILITARY,      SP_MINOR_VOIDSHIP, SP_MAJOR_VOIDSHIP,   SP_INTERROGATION,
               SP_INTIMIDATION,  SP_LEADERSHIP,    SP_LONG_GUNS,      SP_ORNDANCE,         SP_PISTOLS,
               SP_THROWN,        SP_RAP_ANIMALS,   SP_CHARM,          SP_DECEPTION,        SP_HAGGLE,
               SP_INQUIRY,       SP_ACROBATICS,    SP_BALANCE,        SP_DODGE,            SP_CONCEAL,
               SP_HIDE,          SP_MOVE_SILENTLY, SP_AUGMETICS,      SP_ENGINEERING,      SP_SECURITY]

SKILL_SPEC_TAG = 'specializations'

CHAR_STAT_TAG = 'stats'
CHAR_SKILL_TAG = 'skills'
SPECIAL_CHARACTER_TAGS = [CHAR_STAT_TAG, CHAR_SKILL_TAG]
