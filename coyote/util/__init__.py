class Utility:
    """
    This class is used to store all the utility classes that are used in the
    """

    def __init__(self):
        self.variant = None
        self.common = None

    def init_util(self):
        from coyote.blueprints.variants.util import VariantUtility
        from coyote.util.common_utility import CommonUtility
        from coyote.blueprints.main.util import MainUtility
        from coyote.blueprints.rna.util import RNAUtility

        self.variant = VariantUtility()
        self.common = CommonUtility()
        self.main = MainUtility()
        self.rna = RNAUtility()