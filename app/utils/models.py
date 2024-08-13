from typing import List, Dict
from pydantic import BaseModel

class ExtractedSections(BaseModel):
    PRIIPSKIDTypeOption: str
    PRIIPsKIDTerm: str
    PRIIPsKIDObjective: str
    PRIIPsKIDTargetMarket: str
    PRIIPsKIDOtherRisks: str
    PRIIPsKIDUnableToPayOut: str
    PRIIPsKIDTakeMoneyOutEarly: str
    PRIIPsKIDComplaints: str
    PRIIPsKIDOtherInfoEU: str
    PRIIPsKIDEntryCostDescription: str
    PRIIPsKIDExitCostDescription: str
    PRIIPsKIDOngoingCostsDescription: str
    PRIIPsKIDTransactionCostsDescription: str
    PRIIPsKIDPerformanceFeesDescription: str
    