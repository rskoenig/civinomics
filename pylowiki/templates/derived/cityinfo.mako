<%inherit file="/base/template.html" />

<h1>${c.heading}</h1>

<ul>
<li>City is ${c.cityInfo['City']}</li>
<li>County is ${c.cityInfo['County']}</li>
<li>State is ${c.cityInfo['StateFullName']}</li>
</ul>
<p>&nbsp;</p>
<ul>
<li>Population in ${c.cityInfo['City']} is ${c.cityInfo['Population']}</li>
<li>Population_Under5 is ${c.cityInfo['Population_Under5']}</li>
<li>Population_5to9 is ${c.cityInfo['Population_5to9']}</li>
<li>Population_10to14 is ${c.cityInfo['Population_10to14']}</li>
<li>Population_15to19 is ${c.cityInfo['Population_15to19']}</li>
<li>Population_20to24 is ${c.cityInfo['Population_20to24']}</li>
<li>Population_25to29 is ${c.cityInfo['Population_25to29']}</li>
<li>Population_30to34 is ${c.cityInfo['Population_30to34']}</li>
<li>Population_35to39 is ${c.cityInfo['Population_35to39']}</li>
<li>Population_40to44 is ${c.cityInfo['Population_40to44']}</li>
<li>Population_45to49 is ${c.cityInfo['Population_45to49']}</li>
<li>Population_50to54 is ${c.cityInfo['Population_50to54']}</li>
<li>Population_55to59 is ${c.cityInfo['Population_55to59']}</li>
<li>Population_60to64 is ${c.cityInfo['Population_60to64']}</li>
<li>Population_65to69 is ${c.cityInfo['Population_65to69']}</li>
<li>Population_70to74 is ${c.cityInfo['Population_70to74']}</li>
<li>Population_75to79 is ${c.cityInfo['Population_75to79']}</li>
<li>Population_80to84 is ${c.cityInfo['Population_80to84']}</li>
<li>Population_85Plus is ${c.cityInfo['Population_85Plus']}</li>
<li>Population_Median is ${c.cityInfo['Population_Median']}</li>
<li>Population_16Plus is ${c.cityInfo['Population_16Plus']}</li>
<li>Population_18Plus is ${c.cityInfo['Population_18Plus']}</li>
<li>Population_21Plus is ${c.cityInfo['Population_21Plus']}</li>
<li>Population_62Plus is ${c.cityInfo['Population_62Plus']}</li>
<li>Population_65Plus is ${c.cityInfo['Population_65Plus']}</li>
<li>Population_Male is ${c.cityInfo['Population_Male']}</li>
<li>Population_Male_Under5 is ${c.cityInfo['Population_Male_Under5']}</li>
<li>Population_Male_5to9 is ${c.cityInfo['Population_Male_5to9']}</li>
<li>Population_Male_10to14 is ${c.cityInfo['Population_Male_10to14']}</li>
<li>Population_Male_15to19 is ${c.cityInfo['Population_Male_15to19']}</li>
<li>Population_Male_20to24 is ${c.cityInfo['Population_Male_20to24']}</li>
<li>Population_Male_25to29 is ${c.cityInfo['Population_Male_25to29']}</li>
<li>Population_Male_30to34 is ${c.cityInfo['Population_Male_30to34']}</li>
<li>Population_Male_35to39 is ${c.cityInfo['Population_Male_35to39']}</li>
<li>Population_Male_40to44 is ${c.cityInfo['Population_Male_40to44']}</li>
<li>Population_Male_45to49 is ${c.cityInfo['Population_Male_45to49']}</li>
<li>Population_Male_50to54 is ${c.cityInfo['Population_Male_50to54']}</li>
<li>Population_Male_55to59 is ${c.cityInfo['Population_Male_55to59']}</li>
<li>Population_Male_60to64 is ${c.cityInfo['Population_Male_60to64']}</li>
<li>Population_Male_65to69 is ${c.cityInfo['Population_Male_65to69']}</li>
<li>Population_Male_70to74 is ${c.cityInfo['Population_Male_70to74']}</li>
<li>Population_Male_75to79 is ${c.cityInfo['Population_Male_75to79']}</li>
<li>Population_Male_80to84 is ${c.cityInfo['Population_Male_80to84']}</li>
<li>Population_Male_85Plus is ${c.cityInfo['Population_Male_85Plus']}</li>
<li>Population_Male_Median is ${c.cityInfo['Population_Male_Median']}</li>
<li>Population_Male_16Plus is ${c.cityInfo['Population_Male_16Plus']}</li>
<li>Population_Male_18Plus is ${c.cityInfo['Population_Male_18Plus']}</li>
<li>Population_Male_21Plus is ${c.cityInfo['Population_Male_21Plus']}</li>
<li>Population_Male_62Plus is ${c.cityInfo['Population_Male_62Plus']}</li>
<li>Population_Male_65Plus is ${c.cityInfo['Population_Male_65Plus']}</li>
<li>Population_Female is ${c.cityInfo['Population_Female']}</li>
<li>Population_Female_Under5 is ${c.cityInfo['Population_Female_Under5']}</li>
<li>Population_Female_5to9 is ${c.cityInfo['Population_Female_5to9']}</li>
<li>Population_Female_10to14 is ${c.cityInfo['Population_Female_10to14']}</li>
<li>Population_Female_15to19 is ${c.cityInfo['Population_Female_15to19']}</li>
<li>Population_Female_20to24 is ${c.cityInfo['Population_Female_20to24']}</li>
<li>Population_Female_25to29 is ${c.cityInfo['Population_Female_25to29']}</li>
<li>Population_Female_30to34 is ${c.cityInfo['Population_Female_30to34']}</li>
<li>Population_Female_35to39 is ${c.cityInfo['Population_Female_35to39']}</li>
<li>Population_Female_40to44 is ${c.cityInfo['Population_Female_40to44']}</li>
<li>Population_Female_45to49 is ${c.cityInfo['Population_Female_45to49']}</li>
<li>Population_Female_50to54 is ${c.cityInfo['Population_Female_50to54']}</li>
<li>Population_Female_55to59 is ${c.cityInfo['Population_Female_55to59']}</li>
<li>Population_Female_60to64 is ${c.cityInfo['Population_Female_60to64']}</li>
<li>Population_Female_65to69 is ${c.cityInfo['Population_Female_65to69']}</li>
<li>Population_Female_70to74 is ${c.cityInfo['Population_Female_70to74']}</li>
<li>Population_Female_75to79 is ${c.cityInfo['Population_Female_75to79']}</li>
<li>Population_Female_80to84 is ${c.cityInfo['Population_Female_80to84']}</li>
<li>Population_Female_85Plus is ${c.cityInfo['Population_Female_85Plus']}</li>
<li>Population_Female_Median is ${c.cityInfo['Population_Female_Median']}</li>
<li>Population_Female_16Plus is ${c.cityInfo['Population_Female_16Plus']}</li>
<li>Population_Female_18Plus is ${c.cityInfo['Population_Female_18Plus']}</li>
<li>Population_Female_21Plus is ${c.cityInfo['Population_Female_21Plus']}</li>
<li>Population_Female_62Plus is ${c.cityInfo['Population_Female_62Plus']}</li>
<li>Population_Female_65Plus is ${c.cityInfo['Population_Female_65Plus']}</li>
<li>Population_Race_White is ${c.cityInfo['Population_Race_White']}</li>
<li>Population_Race_Black is ${c.cityInfo['Population_Race_Black']}</li>
<li>Population_Race_AmericanIndian is ${c.cityInfo['Population_Race_AmericanIndian']}</li>
<li>Population_Race_Asian is ${c.cityInfo['Population_Race_Asian']}</li>
<li>Population_Race_Hawaiian is ${c.cityInfo['Population_Race_Hawaiian']}</li>
<li>Population_Race_Other is ${c.cityInfo['Population_Race_Other']}</li>
<li>Population_Race_Hispanic is ${c.cityInfo['Population_Race_Hispanic']}</li>
<li>Average_Household_Size is ${c.cityInfo['Average_Household_Size']}</li>
<li>Average_Family_Size is ${c.cityInfo['Average_Family_Size']}</li>
<li>Total_Households is ${c.cityInfo['Total_Households']}</li>
<li>Family_Households is ${c.cityInfo['Family_Households']}</li>
<li>Family_Households_With_Children_Under_18 is ${c.cityInfo['Family_Households_With_Children_Under_18']}</li>
<li>Family_Households_HusbandWife_Family is ${c.cityInfo['Family_Households_HusbandWife_Family']}</li>
<li>Family_Households_HusbandWife_Family_Children_Under18 is ${c.cityInfo['Family_Households_HusbandWife_Family_Children_Under18']}</li>
<li>Family_Households_Male_No_Wife is ${c.cityInfo['Family_Households_Male_No_Wife']}</li>
<li>Family_Households_Male_No_Wife_Children_Under18 is ${c.cityInfo['Family_Households_Male_No_Wife_Children_Under18']}</li>
<li>Family_Household_Female_No_Husband is ${c.cityInfo['Family_Household_Female_No_Husband']}</li>
<li>Family_Household_Female_No_Husband_Children_Under18 is ${c.cityInfo['Family_Household_Female_No_Husband_Children_Under18']}</li>
<li>Non_Family_Households is ${c.cityInfo['Non_Family_Households']}</li>
<li>Non_Family_Households_Living_Alone is ${c.cityInfo['Non_Family_Households_Living_Alone']}</li>
<li>Non_Family_Households_Living_Alone_Male is ${c.cityInfo['Non_Family_Households_Living_Alone_Male']}</li>
<li>Non_Family_Households_Living_Alone_Male_65plus is ${c.cityInfo['Non_Family_Households_Living_Alone_Male_65plus']}</li>
<li>Non_Family_Households_Living_Alone_Female is ${c.cityInfo['Non_Family_Households_Living_Alone_Female']}</li>
<li>Non_Family_Households_Living_Alone_Female_65plus is ${c.cityInfo['Non_Family_Households_Living_Alone_Female_65plus']}</li>
<li>Households_With_Individuals_Under_18 is ${c.cityInfo['Households_With_Individuals_Under_18']}</li>
<li>Households_With_Individuals_65plus is ${c.cityInfo['Households_With_Individuals_65plus']}</li>
<li>Total_Housing_Units is ${c.cityInfo['Total_Housing_Units']}</li>
<li>Occupied_Housing_Units is ${c.cityInfo['Occupied_Housing_Units']}</li>
<li>Vacant_Housing_Units is ${c.cityInfo['Vacant_Housing_Units']}</li>
<li>Vacant_Housing_Units_For_Rent is ${c.cityInfo['Vacant_Housing_Units_For_Rent']}</li>
<li>Vacant_Housing_Units_Rented_Not_Occupied is ${c.cityInfo['Vacant_Housing_Units_Rented_Not_Occupied']}</li>
<li>Vacant_Housing_Units_For_Sale is ${c.cityInfo['Vacant_Housing_Units_For_Sale']}</li>
<li>Vacant_Housing_Units_Sold_Not_Occupied is ${c.cityInfo['Vacant_Housing_Units_Sold_Not_Occupied']}</li>
<li>Vacant_Housing_Units_For_Seasonal_Occasional_Use is ${c.cityInfo['Vacant_Housing_Units_For_Seasonal_Occasional_Use']}</li>
<li>Vacant_Housing_Units_All_Other_Vacants is ${c.cityInfo['Vacant_Housing_Units_All_Other_Vacants']}</li>
</ul>

<%def name = 'extraStyles()'>
	
</%def>

<%def name = 'extraScripts()'>
	
</%def>

<%def name = 'extraHTML()'>

</%def>
