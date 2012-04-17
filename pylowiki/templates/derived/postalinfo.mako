<%inherit file="/base/template.html" />

<h1>${c.heading}</h1>

<ul>
<li>Zip is ${c.postalInfo['ZipCode']}</li>
<li>City is ${c.postalInfo['City']}</li>
<li>County is ${c.postalInfo['County']}</li>
<li>State is ${c.postalInfo['StateFullName']}</li>
</ul>
<p>&nbsp;</p>
<ul>
<li>Population in ${c.postalInfo['ZipCode']} is ${c.postalInfo['Population']}</li>
<li>White  Population is ${c.postalInfo['WhitePopulation']}</li>
<li>Black Population is ${c.postalInfo['BlackPopulation']}</li>
<li>Hispanic Population is ${c.postalInfo['HispanicPopulation']}</li>
<li>Asian Population is ${c.postalInfo['AsianPopulation']}</li>
<li>Hawaiian Population is ${c.postalInfo['HawaiianPopulation']}</li>
<li>Indian Population is ${c.postalInfo['IndianPopulation']}</li>
<li>Other Population is ${c.postalInfo['OtherPopulation']}</li>
<li>Male Population is ${c.postalInfo['MalePopulation']}</li>
<li>Female Population is ${c.postalInfo['FemalePopulation']}</li>
</ul>
<p>&nbsp;</p>
<ul>
<li>Median Age is ${c.postalInfo['MedianAge']}</li>
<li>Median Age Male is ${c.postalInfo['MedianAgeMale']}</li>
<li>Median Age Female is ${c.postalInfo['MedianAgeFemale']}</li>
</ul>
<p>&nbsp;</p>
<ul>
<li>Number of Households is ${c.postalInfo['HouseholdsPerZipCode']}</li>
<li>Persons per Household is ${c.postalInfo['PersonsPerHousehold']}</li>
<li>Average House Value is ${c.postalInfo['AverageHouseValue']}</li>
<li>Income Per Household is ${c.postalInfo['IncomePerHousehold']}</li>
<li>Median Age is ${c.postalInfo['MedianAge']}</li>
</ul>
<p>&nbsp;</p>
<ul>
<li>Latitude is ${c.postalInfo['Latitude']}</li>
<li>Longitude is ${c.postalInfo['Longitude']}</li>
<li>Elevation is ${c.postalInfo['Elevation']}</li>
</ul>
<p>&nbsp;</p>
<ul>
<li>State is ${c.postalInfo['State']}</li>
<li>State Full Name is ${c.postalInfo['StateFullName']}</li>
<li>City Type is ${c.postalInfo['CityType']}</li>
<li>City Alias Abbreviation is ${c.postalInfo['CityAliasAbbreviation']}</li>
<li>Area Code is ${c.postalInfo['AreaCode']}</li>
<li>City is ${c.postalInfo['City']}</li>
<li>City Alias Name is ${c.postalInfo['CityAliasName']}</li>
<li>County is ${c.postalInfo['County']}</li>
<li>County FIPS is ${c.postalInfo['CountyFIPS']}</li>
<li>State FIPS is ${c.postalInfo['StateFIPS']}</li>
<li>Time Zone is ${c.postalInfo['TimeZone']}</li>
<li>Daylight Savings Time is ${c.postalInfo['DayLightSaving']}</li>
<li>MSA is ${c.postalInfo['MSA']}</li>
<li>PMSA is ${c.postalInfo['PMSA']}</li>
<li>CSA is ${c.postalInfo['CSA']}</li>
<li>CBSA is ${c.postalInfo['CBSA']}</li>
<li>CBSA Div is ${c.postalInfo['CBSA_Div']}</li>
<li>CBSA Type is ${c.postalInfo['CBSA_Type']}</li>
<li>CBSA Name is ${c.postalInfo['CBSA_Name']}</li>
<li>MSA Name is ${c.postalInfo['MSA_Name']}</li>
<li>PMSA Name is ${c.postalInfo['PMSA_Name']}</li>
<li>Region is ${c.postalInfo['Region']}</li>
<li>Division is ${c.postalInfo['Division']}</li>
<li>Mailing Name is ${c.postalInfo['MailingName']}</li>
<li>Number of Businesses is ${c.postalInfo['NumberOfBusinesses']}</li>
<li>Number of Employees is ${c.postalInfo['NumberOfEmployees']}</li>
<li>Business First Quarter Payroll is ${c.postalInfo['BusinessFirstQuarterPayroll']}</li>
<li>Business Annual Payroll is ${c.postalInfo['BusinessAnnualPayroll']}</li>
<li>Business Employment Flag is ${c.postalInfo['BusinessEmploymentFlag']}</li>
<li>Growth Rank is ${c.postalInfo['GrowthRank']}</li>
<li>Growth Housing Units 2003 is ${c.postalInfo['GrowthHousingUnits2003']}</li>
<li>Growth Housing Units 2004 is ${c.postalInfo['GrowthHousingUnits2004']}</li>
<li>Growth Increase Number is ${c.postalInfo['GrowthIncreaseNumber']}</li>
<li>CBSA Population 2003 is ${c.postalInfo['CBSAPop2003']}</li>
<li>CBSA Division Population 2003 is ${c.postalInfo['CBSADivPop2003']}</li>
<li>Congressional District is ${c.postalInfo['CongressionalDistrict']}</li>
<li>Congressional Land Area is ${c.postalInfo['CongressionalLandArea']}</li>
<li>Residential Delivery is ${c.postalInfo['DeliveryResidential']}</li>
<li>Business Delivery is ${c.postalInfo['DeliveryBusiness']}</li>
<li>Total Delivery is ${c.postalInfo['DeliveryTotal']}</li>
<li>Preferred Last Line Key is ${c.postalInfo['PreferredLastLineKey']}</li>
<li>Classification Code is ${c.postalInfo['ClassificationCode']}</li>
<li>Multi-County is ${c.postalInfo['MultiCounty']}</li>
<li>CSA Name is ${c.postalInfo['CSAName']}</li>
<li>CBSA Division Name is ${c.postalInfo['CBSA_Div_Name']}</li>
<li>City State Key is ${c.postalInfo['CityStateKey']}</li>
<li>Population Estimate is ${c.postalInfo['PopulationEstimate']}</li>
<li>Land Area is ${c.postalInfo['LandArea']} square miles</li>
<li>Water Area is ${c.postalInfo['WaterArea']} square miles</li>
<li>City Alias Code is ${c.postalInfo['CityAliasCode']}</li>
<li>City Mixed Case is ${c.postalInfo['CityMixedCase']}</li>
<li>City Alias Mixed Case is ${c.postalInfo['CityAliasMixedCase']}</li>
<li>Box Count is ${c.postalInfo['BoxCount']}</li>
<li>SFDU is ${c.postalInfo['SFDU']}</li>
<li>MFDU is ${c.postalInfo['MFDU']}</li>
<li>State ANSI is ${c.postalInfo['StateANSI']}</li>
<li>County ANSI is ${c.postalInfo['CountyANSI']}</li>
<li>Alias Intro Date is ${c.postalInfo['AliasIntroDate']}</li>
<li>Facility Code is ${c.postalInfo['FacilityCode']}</li>
<li>City Delivery Indicator is ${c.postalInfo['CityDeliveryIndicator']}</li>
<li>Carrier Route Rate Sortation is ${c.postalInfo['CarrierRouteRateSortation']}</li>
<li>Finance Number is ${c.postalInfo['FinanceNumber']}</li>
</ul>

<%def name = 'extraStyles()'>
	
</%def>

<%def name = 'extraScripts()'>
	
</%def>

<%def name = 'extraHTML()'>

</%def>
