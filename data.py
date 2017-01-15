

class Chapter:
    pass


class Introduction(Chapter):
    slug = 'introduction'
    name = 'Introduction'
    id_string = None


class Chapter1(Chapter):
    slug = 'building-blocks-of-reentry'
    name = 'Building Blocks of Reentry'
    id_string = "CHAPTER1_ID"


class Chapter2(Chapter):
    slug = 'parole-and-probation'
    name = 'Parole &amp; Probation'
    id_string = "CHAPTER2_PP"


class Chapter3(Chapter):
    slug = 'housing'
    name = 'Housing'
    id_string = "CHAPTER4_HS"


class Chapter4(Chapter):
    slug = 'public-benefits'
    name = 'Public Benefits'
    id_string = "CHAPTER5_PB"


class Chapter5(Chapter):
    slug = 'employment'
    name = 'Employment'
    id_string = "CHAPTER6_EM"


class Chapter6(Chapter):
    slug = 'court-ordered-debt'
    name = 'Court-ordered Debt'
    id_string = "CHAPTER7_COD"


class Chapter7(Chapter):
    slug = 'family-and-children'
    name = 'Family &amp; Children'
    id_string = "CHAPTER8_FC"


class Chapter8(Chapter):
    slug = 'education'
    name = 'Education'
    id_string = "CHAPTER9_ED"


class Chapter9(Chapter):
    slug = 'your-criminal-record'
    name = 'Understanding &amp; Cleaning Up Your Criminal Record'
    id_string = "CHAPTER3_EX"


class Appendix(Chapter):
    slug = 'legal-aid-providers'
    name = 'Legal Aid Providers'
    id_string = "App_LegalAidProvidersList"


class Appendix2(Chapter):
    slug = 'ca-social-services'
    name = 'California Social Services'
    id_string = "App_CommunityResourceList"


ALL_CHAPTERS = [
    Introduction,
    Chapter1,
    Chapter2,
    Chapter3,
    Chapter4,
    Chapter5,
    Chapter6,
    Chapter7,
    Chapter8,
    Chapter9,
    Appendix,
    Appendix2,
]
