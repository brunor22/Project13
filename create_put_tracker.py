#!/usr/bin/env python3
"""
Create a Put Selling Tracker Excel spreadsheet without external dependencies.
An xlsx file is a zip archive containing XML files.
"""

import zipfile
import os
from datetime import datetime

def create_xlsx(filename):
    """Create an Excel xlsx file for tracking put selling transactions."""

    # Content Types XML
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
    <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
    <Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
</Types>'''

    # Relationships
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''

    # Workbook relationships
    workbook_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>
    <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
    <Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>'''

    # Workbook
    workbook = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
    <sheets>
        <sheet name="Put Trades" sheetId="1" r:id="rId1"/>
        <sheet name="Stock Positions" sheetId="2" r:id="rId2"/>
        <sheet name="Summary" sheetId="3" r:id="rId3"/>
    </sheets>
</workbook>'''

    # Styles with formatting for currency, dates, percentages, and headers
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <numFmts count="4">
        <numFmt numFmtId="164" formatCode="&quot;$&quot;#,##0.00"/>
        <numFmt numFmtId="165" formatCode="yyyy-mm-dd"/>
        <numFmt numFmtId="166" formatCode="0.00%"/>
        <numFmt numFmtId="167" formatCode="#,##0"/>
    </numFmts>
    <fonts count="3">
        <font><sz val="11"/><name val="Calibri"/></font>
        <font><b/><sz val="11"/><name val="Calibri"/></font>
        <font><b/><sz val="14"/><name val="Calibri"/></font>
    </fonts>
    <fills count="4">
        <fill><patternFill patternType="none"/></fill>
        <fill><patternFill patternType="gray125"/></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FF4472C4"/></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FFE2EFDA"/></patternFill></fill>
    </fills>
    <borders count="2">
        <border/>
        <border>
            <left style="thin"><color auto="1"/></left>
            <right style="thin"><color auto="1"/></right>
            <top style="thin"><color auto="1"/></top>
            <bottom style="thin"><color auto="1"/></bottom>
        </border>
    </borders>
    <cellStyleXfs count="1">
        <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
    </cellStyleXfs>
    <cellXfs count="10">
        <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
        <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"><alignment horizontal="center"/></xf>
        <xf numFmtId="164" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
        <xf numFmtId="165" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
        <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"/>
        <xf numFmtId="166" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
        <xf numFmtId="167" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
        <xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"/>
        <xf numFmtId="0" fontId="1" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"/>
        <xf numFmtId="164" fontId="1" fillId="3" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1" applyBorder="1"/>
    </cellXfs>
</styleSheet>'''

    # Shared strings - all text values used in the spreadsheet
    shared_strings_list = [
        # Sheet 1: Put Trades headers (0-16)
        "Trade ID", "Open Date", "Ticker", "Strike Price", "Expiration Date",
        "Contracts", "Premium/Contract", "Total Premium", "Commission", "Net Credit",
        "Status", "Close Date", "Close Price", "Close Commission", "Net P&L",
        "Assignment Date", "Notes",
        # Sheet 2: Stock Positions headers (17-29)
        "Position ID", "Source Trade ID", "Ticker", "Acquisition Date", "Shares",
        "Cost Basis/Share", "Total Cost Basis", "Sale Date", "Sale Price/Share",
        "Gross Proceeds", "Sale Commission", "Net Proceeds", "Stock P&L",
        # Sheet 3: Summary labels (30-50)
        "PUT SELLING TRACKER - SUMMARY", "Overall Statistics", "Total Trades",
        "Open Trades", "Closed Trades", "Expired (Profit)", "Assigned", "Win Rate",
        "Premium Statistics", "Total Premium Collected", "Total Commissions Paid",
        "Net Premium (Closed Trades)", "Realized P&L from Puts", "Stock Position Statistics",
        "Total Positions", "Open Positions", "Closed Positions", "Realized Stock P&L",
        "Combined Statistics", "Total Realized P&L", "Unrealized Stock Value",
        # Status values (51-54)
        "Open", "Closed", "Expired", "Assigned",
        # Example data descriptions (55-57)
        "Example: Sold put on AAPL", "Example: Assigned and sold", "Example: Expired worthless"
    ]

    shared_strings = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(shared_strings_list)}" uniqueCount="{len(shared_strings_list)}">
'''
    for s in shared_strings_list:
        shared_strings += f'    <si><t>{s}</t></si>\n'
    shared_strings += '</sst>'

    # Sheet 1: Put Trades
    sheet1 = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheetViews>
        <sheetView tabSelected="1" workbookViewId="0">
            <pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>
        </sheetView>
    </sheetViews>
    <cols>
        <col min="1" max="1" width="10" customWidth="1"/>
        <col min="2" max="2" width="12" customWidth="1"/>
        <col min="3" max="3" width="10" customWidth="1"/>
        <col min="4" max="4" width="12" customWidth="1"/>
        <col min="5" max="5" width="14" customWidth="1"/>
        <col min="6" max="6" width="10" customWidth="1"/>
        <col min="7" max="7" width="16" customWidth="1"/>
        <col min="8" max="8" width="14" customWidth="1"/>
        <col min="9" max="9" width="12" customWidth="1"/>
        <col min="10" max="10" width="12" customWidth="1"/>
        <col min="11" max="11" width="10" customWidth="1"/>
        <col min="12" max="12" width="12" customWidth="1"/>
        <col min="13" max="13" width="12" customWidth="1"/>
        <col min="14" max="14" width="14" customWidth="1"/>
        <col min="15" max="15" width="12" customWidth="1"/>
        <col min="16" max="16" width="14" customWidth="1"/>
        <col min="17" max="17" width="30" customWidth="1"/>
    </cols>
    <sheetData>
        <row r="1">
            <c r="A1" s="1" t="s"><v>0</v></c>
            <c r="B1" s="1" t="s"><v>1</v></c>
            <c r="C1" s="1" t="s"><v>2</v></c>
            <c r="D1" s="1" t="s"><v>3</v></c>
            <c r="E1" s="1" t="s"><v>4</v></c>
            <c r="F1" s="1" t="s"><v>5</v></c>
            <c r="G1" s="1" t="s"><v>6</v></c>
            <c r="H1" s="1" t="s"><v>7</v></c>
            <c r="I1" s="1" t="s"><v>8</v></c>
            <c r="J1" s="1" t="s"><v>9</v></c>
            <c r="K1" s="1" t="s"><v>10</v></c>
            <c r="L1" s="1" t="s"><v>11</v></c>
            <c r="M1" s="1" t="s"><v>12</v></c>
            <c r="N1" s="1" t="s"><v>13</v></c>
            <c r="O1" s="1" t="s"><v>14</v></c>
            <c r="P1" s="1" t="s"><v>15</v></c>
            <c r="Q1" s="1" t="s"><v>16</v></c>
        </row>
        <row r="2">
            <c r="A2" s="4"><v>1</v></c>
            <c r="B2" s="3"><v>45658</v></c>
            <c r="C2" s="4" t="s"><v>55</v></c>
            <c r="D2" s="2"><v>150</v></c>
            <c r="E2" s="3"><v>45688</v></c>
            <c r="F2" s="6"><v>1</v></c>
            <c r="G2" s="2"><v>2.50</v></c>
            <c r="H2" s="2"><f>F2*G2*100</f></c>
            <c r="I2" s="2"><v>1.00</v></c>
            <c r="J2" s="2"><f>H2-I2</f></c>
            <c r="K2" s="4" t="s"><v>53</v></c>
            <c r="L2" s="3"><v>45688</v></c>
            <c r="M2" s="2"><v>0</v></c>
            <c r="N2" s="2"><v>0</v></c>
            <c r="O2" s="2"><f>J2-(M2*F2*100)-N2</f></c>
            <c r="P2" s="3"/>
            <c r="Q2" s="4" t="s"><v>57</v></c>
        </row>
        <row r="3">
            <c r="A3" s="4"><v>2</v></c>
            <c r="B3" s="3"><v>45660</v></c>
            <c r="C3" s="4" t="s"><v>56</v></c>
            <c r="D3" s="2"><v>100</v></c>
            <c r="E3" s="3"><v>45690</v></c>
            <c r="F3" s="6"><v>2</v></c>
            <c r="G3" s="2"><v>3.00</v></c>
            <c r="H3" s="2"><f>F3*G3*100</f></c>
            <c r="I3" s="2"><v>2.00</v></c>
            <c r="J3" s="2"><f>H3-I3</f></c>
            <c r="K3" s="4" t="s"><v>54</v></c>
            <c r="L3" s="3"><v>45685</v></c>
            <c r="M3" s="2"><v>0</v></c>
            <c r="N3" s="2"><v>0</v></c>
            <c r="O3" s="2"><f>J3-(M3*F3*100)-N3</f></c>
            <c r="P3" s="3"><v>45685</v></c>
            <c r="Q3" s="4" t="s"><v>56</v></c>
        </row>
    </sheetData>
    <dataValidations count="1">
        <dataValidation type="list" allowBlank="1" showInputMessage="1" showErrorMessage="1" sqref="K2:K1000">
            <formula1>"Open,Closed,Expired,Assigned"</formula1>
        </dataValidation>
    </dataValidations>
</worksheet>'''

    # Sheet 2: Stock Positions
    sheet2 = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheetViews>
        <sheetView workbookViewId="0">
            <pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>
        </sheetView>
    </sheetViews>
    <cols>
        <col min="1" max="1" width="12" customWidth="1"/>
        <col min="2" max="2" width="14" customWidth="1"/>
        <col min="3" max="3" width="10" customWidth="1"/>
        <col min="4" max="4" width="14" customWidth="1"/>
        <col min="5" max="5" width="10" customWidth="1"/>
        <col min="6" max="6" width="14" customWidth="1"/>
        <col min="7" max="7" width="14" customWidth="1"/>
        <col min="8" max="8" width="12" customWidth="1"/>
        <col min="9" max="9" width="14" customWidth="1"/>
        <col min="10" max="10" width="14" customWidth="1"/>
        <col min="11" max="11" width="14" customWidth="1"/>
        <col min="12" max="12" width="12" customWidth="1"/>
        <col min="13" max="13" width="12" customWidth="1"/>
    </cols>
    <sheetData>
        <row r="1">
            <c r="A1" s="1" t="s"><v>17</v></c>
            <c r="B1" s="1" t="s"><v>18</v></c>
            <c r="C1" s="1" t="s"><v>19</v></c>
            <c r="D1" s="1" t="s"><v>20</v></c>
            <c r="E1" s="1" t="s"><v>21</v></c>
            <c r="F1" s="1" t="s"><v>22</v></c>
            <c r="G1" s="1" t="s"><v>23</v></c>
            <c r="H1" s="1" t="s"><v>24</v></c>
            <c r="I1" s="1" t="s"><v>25</v></c>
            <c r="J1" s="1" t="s"><v>26</v></c>
            <c r="K1" s="1" t="s"><v>27</v></c>
            <c r="L1" s="1" t="s"><v>28</v></c>
            <c r="M1" s="1" t="s"><v>29</v></c>
        </row>
        <row r="2">
            <c r="A2" s="4"><v>1</v></c>
            <c r="B2" s="4"><v>2</v></c>
            <c r="C2" s="4" t="s"><v>56</v></c>
            <c r="D2" s="3"><v>45685</v></c>
            <c r="E2" s="6"><v>200</v></c>
            <c r="F2" s="2"><v>100</v></c>
            <c r="G2" s="2"><f>E2*F2</f></c>
            <c r="H2" s="3"><v>45700</v></c>
            <c r="I2" s="2"><v>110</v></c>
            <c r="J2" s="2"><f>E2*I2</f></c>
            <c r="K2" s="2"><v>10</v></c>
            <c r="L2" s="2"><f>J2-K2</f></c>
            <c r="M2" s="2"><f>L2-G2</f></c>
        </row>
    </sheetData>
</worksheet>'''

    # Sheet 3: Summary with formulas
    sheet3 = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <cols>
        <col min="1" max="1" width="30" customWidth="1"/>
        <col min="2" max="2" width="18" customWidth="1"/>
    </cols>
    <sheetData>
        <row r="1">
            <c r="A1" s="7" t="s"><v>30</v></c>
        </row>
        <row r="3">
            <c r="A3" s="8" t="s"><v>31</v></c>
            <c r="B3" s="8"/>
        </row>
        <row r="4">
            <c r="A4" s="4" t="s"><v>32</v></c>
            <c r="B4" s="6"><f>COUNTA('Put Trades'!A2:A1000)</f></c>
        </row>
        <row r="5">
            <c r="A5" s="4" t="s"><v>33</v></c>
            <c r="B5" s="6"><f>COUNTIF('Put Trades'!K2:K1000,"Open")</f></c>
        </row>
        <row r="6">
            <c r="A6" s="4" t="s"><v>34</v></c>
            <c r="B6" s="6"><f>COUNTIF('Put Trades'!K2:K1000,"Closed")</f></c>
        </row>
        <row r="7">
            <c r="A7" s="4" t="s"><v>35</v></c>
            <c r="B7" s="6"><f>COUNTIF('Put Trades'!K2:K1000,"Expired")</f></c>
        </row>
        <row r="8">
            <c r="A8" s="4" t="s"><v>36</v></c>
            <c r="B8" s="6"><f>COUNTIF('Put Trades'!K2:K1000,"Assigned")</f></c>
        </row>
        <row r="9">
            <c r="A9" s="4" t="s"><v>37</v></c>
            <c r="B9" s="5"><f>IF(B4-B5&gt;0,(B6+B7)/(B4-B5),0)</f></c>
        </row>
        <row r="11">
            <c r="A11" s="8" t="s"><v>38</v></c>
            <c r="B11" s="8"/>
        </row>
        <row r="12">
            <c r="A12" s="4" t="s"><v>39</v></c>
            <c r="B12" s="2"><f>SUM('Put Trades'!H2:H1000)</f></c>
        </row>
        <row r="13">
            <c r="A13" s="4" t="s"><v>40</v></c>
            <c r="B13" s="2"><f>SUM('Put Trades'!I2:I1000)+SUM('Put Trades'!N2:N1000)</f></c>
        </row>
        <row r="14">
            <c r="A14" s="4" t="s"><v>41</v></c>
            <c r="B14" s="2"><f>SUMIF('Put Trades'!K2:K1000,"&lt;&gt;Open",'Put Trades'!J2:J1000)</f></c>
        </row>
        <row r="15">
            <c r="A15" s="4" t="s"><v>42</v></c>
            <c r="B15" s="9"><f>SUMIF('Put Trades'!K2:K1000,"&lt;&gt;Open",'Put Trades'!O2:O1000)</f></c>
        </row>
        <row r="17">
            <c r="A17" s="8" t="s"><v>43</v></c>
            <c r="B17" s="8"/>
        </row>
        <row r="18">
            <c r="A18" s="4" t="s"><v>44</v></c>
            <c r="B18" s="6"><f>COUNTA('Stock Positions'!A2:A1000)</f></c>
        </row>
        <row r="19">
            <c r="A19" s="4" t="s"><v>45</v></c>
            <c r="B19" s="6"><f>COUNTBLANK('Stock Positions'!H2:H1000)</f></c>
        </row>
        <row r="20">
            <c r="A20" s="4" t="s"><v>46</v></c>
            <c r="B20" s="6"><f>B18-B19</f></c>
        </row>
        <row r="21">
            <c r="A21" s="4" t="s"><v>47</v></c>
            <c r="B21" s="9"><f>SUM('Stock Positions'!M2:M1000)</f></c>
        </row>
        <row r="23">
            <c r="A23" s="8" t="s"><v>48</v></c>
            <c r="B23" s="8"/>
        </row>
        <row r="24">
            <c r="A24" s="4" t="s"><v>49</v></c>
            <c r="B24" s="9"><f>B15+B21</f></c>
        </row>
    </sheetData>
</worksheet>'''

    # Create the xlsx file
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('xl/_rels/workbook.xml.rels', workbook_rels)
        zf.writestr('xl/workbook.xml', workbook)
        zf.writestr('xl/styles.xml', styles)
        zf.writestr('xl/sharedStrings.xml', shared_strings)
        zf.writestr('xl/worksheets/sheet1.xml', sheet1)
        zf.writestr('xl/worksheets/sheet2.xml', sheet2)
        zf.writestr('xl/worksheets/sheet3.xml', sheet3)

    print(f"Created: {filename}")
    print("\nSpreadsheet contains 3 sheets:")
    print("1. Put Trades - Track all put selling transactions")
    print("2. Stock Positions - Track stocks acquired through assignment")
    print("3. Summary - Overview with calculated statistics")
    print("\nFeatures:")
    print("- Automatic P&L calculations with formulas")
    print("- Status dropdown (Open/Closed/Expired/Assigned)")
    print("- Currency formatting for dollar amounts")
    print("- Date formatting")
    print("- Frozen header rows")
    print("- Sample data included as examples")

if __name__ == "__main__":
    output_file = "/home/user/Project13/Put_Selling_Tracker.xlsx"
    create_xlsx(output_file)
