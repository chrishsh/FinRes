class RegulatoryComplianceEngine:
    def __init__(self, locate_engine):
        self.locate_engine = locate_engine
        self.violations = []
        
    def validate_exposure(self, net_exposure_df):
        validated_records = []
        for _, row in net_exposure_df.iterrows():
            record = row.to_dict()
            record['Compliance_Status'] = 'Passed'
            
            if row['Quantity'] < 0: # Short position
                if row['Jurisdiction'] == 'US':
                    # Reg SHO Check
                    locate = self.locate_engine.get_locate(row['Ticker'], abs(row['Quantity']))
                    if not locate['Secured']:
                        record['Compliance_Status'] = 'REJECTED: Reg SHO No Locate'
                        self.violations.append(record)
                        continue
                    record['Locate_ID'] = locate['Locate_ID']
                    record['Borrow_Fee_Rate'] = locate['Borrow_Fee_Rate']
                elif row['Jurisdiction'] == 'APAC':
                    # APAC Naked Short Check (Mock SBL failure for specific ticker to show logic)
                    if '0700.HK' in row['Ticker']:
                        record['Compliance_Status'] = 'REJECTED: APAC Naked Short Ban'
                        self.violations.append(record)
                        continue
                    record['Locate_ID'] = 'SBL_PRE_BORROW_OK'
                    record['Borrow_Fee_Rate'] = 0.02 # Flat 2% for APAC shorts
            
            validated_records.append(record)
            
        import pandas as pd
        return pd.DataFrame(validated_records)
