import logging
import glob

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

import pylowiki.lib.helpers as h

from pylowiki.lib.base import BaseController, render

log = logging.getLogger(__name__)

class CorpController(BaseController):
    
    def index(self):
        c.title = 'About us'
        return render('/derived/corp_about.bootstrap')

    def about(self):
        c.title = 'About'
        c.pagetype="about" 
        return render('/derived/corp_about.bootstrap')

    def caseStudies(self):
        c.pagetype="caseStudies"  
        c.title="Surveys"

        c.clients=[]
        client={}
        client['name']="San Francisco Public Utilities Commission"
        client['logo']="sfpuc_small.jpg"
        client['url']='SSIP'
        c.clients.append(client)
        client={}
        client['name']="Soquel Creek Water District"
        client['logo']="soquelCreek_small.jpg"
        client['url']='scwd2'
        c.clients.append(client)
        client={}
        client['name']="Land Trust of Santa Cruz County"
        client['logo']="landTrust_small.jpg"
        client['url']='landtrust'
        c.clients.append(client)
        client={}
        client['name']="Santa Cruz Area Chamber of Commerce"
        client['logo']="scChamber_small.jpg"
        client['url']='#'
        c.clients.append(client)
        client={}
        client['name']="City of Santa Cruz"
        client['logo']="santaCruz_small.jpg"
        client['url']='cap2'
        c.clients.append(client)
        client={}
        client['name']="University of California Santa Cruz"
        client['logo']="ucsc.jpg"
        client['url']='#'
        c.clients.append(client)


        c.studies=[]

        study={}
        study["title"]="Scotts Valley Plastic Bag Ban Opinion Poll"
        study["description"]="Conducted via door-to-door interviews of registered voters."
        study["image"]="bagCreek.jpg"
        study["url"]="svbagban"
        study['date']="4.9.14"
        study['stats']='plasticBagBan'
        study['respondents'] = 397
        study['partnerLogo']='sosLogo.jpg'
        study['partnerName']='Save Our shores'
        study['scope'] = ''
        study['tag'] = ''
        c.studies.append(study)

        study={}
        study["title"]="Downtown Management Corporation - Customer Feedback Survey"
        study["description"]="A survey of Pacific Ave. business owners regarding the efficacy of the Host Program at creating a safe environment downtown."
        study["image"]="hostPic.png"
        study["url"]="dmc"
        study['date']="4.8.14"
        study['stats']='dcDmcSurvey'
        study['respondents'] = 183
        study['clientLogo']='dmcLogo.png'
        study['cientName']='Downtown Management Corporation of Santa Cruz'
        study['scope'] = ''
        study['tag'] = ''
        c.studies.append(study)

        study={}
        study["title"]="Santa Cruz Tech Commuters"
        study["description"]="Measuring Santa Cruz County's daily tech worker brain drain and awareness, opportunity and feedback on the emerging Santa Cruz tech ecosystem."
        study["image"]="techCommuter.png"
        study["url"]="techCommuter"
        study['date']="3.25.14"
        study['stats']='dcCommuterSurvey'
        study['respondents'] = 102
        study['partnerLogo']='ssvLogo.png'
        study['partnerName']='South Swell Ventures'
        study['scope'] = ''
        study['tag'] = ''
        c.studies.append(study)

        study={}
        study["title"]="Sewer System Improvement Program"
        study["description"]="Planning for a multi-billion dollar upgrade to San Francisco's sewer system"
        study["image"]="ssipCover.png"
        study["url"]="SSIP"
        study['date']="3.4.13"
        study['stats']='dcCommuterSurvey'
        study['respondents'] = 1200
        study['clientLogo']='sfpucLogo.png'
        study['clientName']='San Francisco Public Utilities Commission'
        c.studies.append(study)

        study={}
        study["title"]="Eastside Recycled Water Project"
        study["description"]="Siting a new facility to produce recycled water for San Francisco's Downtown"
        study["image"]="eastsideProject.png"
        study["url"]="eastsideProject"
        study['date']="10.10.12"
        study['respondents'] = 934
        study['clientLogo']='sfpucLogo.png'
        study['clientName']='San Francisco Public Utilities Commission'
        c.studies.append(study)

        study={}
        study["title"]="Santa Cruz Climate Action Plan"
        study["description"]="Implenting the City's plan to reduce carbon emissions 30% by 2020"
        study["image"]="CAP.png"
        study["url"]="cap2"
        study['date']="9.11.12"
        study['respondents'] = 500
        study['clientLogo']='scCAP.jpg'
        study['clientName']='City of Santa Cruz Climate Action Plan'
        study['sponsorLogo']='allterraSolar.jpg'
        study['sponsorName']='Allterra Solar'
        c.studies.append(study)

        study={}
        study["title"]="Campaign for 10,000 Acres"
        study["description"]="Collecting ideas on how to save Santa Cruz County's highest priority conservation land"
        study["image"]="landTrust.png"
        study["url"]="landtrust"
        study['respondents'] = 500
        study['clientLogo']='landTrustLogo.jpg'
        study['clientName']='City of Santa Cruz Climate Action Plan'
        study['date']="7.2.12"
        c.studies.append(study)

        study={}
        study["title"]="Santa Cruz and Soquel Creek Water Planning"
        study["description"]="Raising awareness about the regions' water shortage and a proposed desalination plant"
        study["image"]="scwd2Cover.png"
        study["url"]="scwd2"
        study['date']="4.10.12"
        study['respondents'] = 1538
        study['clientLogo']='soquelCreek.gif'
        study['clientName']='Soquel Creek Water District'
        c.studies.append(study)

        return render("/derived/corp_listStudies.bootstrap")


    def polling(self):
        c.pagetype="polling"  
        c.title="Polling"

        c.reports=[]
        report={}
        report["title"]="Santa Cruz County Bag Ban at One Year"
        report["url"]="SOS_BanAnniversary_PollResults.pdf"
        report['partner']='Partner: Save Our Shores'
        report['date']="3.22.13"
        c.reports.append(report)
        report={}
        report["title"]="Santa Cruz County Business Fair 2013"
        report["url"]="BizFair_2013_Results.pdf"
        report['partner']='Partner: Santa Cruz Area Chamber of Commerce'
        report['date']="3.14.13"
        c.reports.append(report)
        report={}
        report["title"]="Santa Cruz Climate Action Plan - Initial Funding and Policy Option"
        report["url"]="CAP_PublicReport_091112.pdf"
        report['partner']='Partner: City of Santa Cruz'
        report['date']="9.11.12"
        c.reports.append(report)

        return render("/derived/corp_polling.bootstrap")


    def displayCaseStudy(self, id):
        c.pagetype="caseStudies"  
        c.title="Surveys"

        casestudyname=id
        study={}
        c.study=study 
        if casestudyname=="scwd2":
            study["url"]="scwd2"
            study["title"]="Santa Cruz and Soquel Creek Water Planning"
            study["image"]="scwd2_splash_1.26.001.png"
            study["statusType"]="important"
            study["statusMessage"]="Closed"
            study["date"]="3-25-2012"
            study["background"]="The City of Santa Cruz and the Soquel Creek Water District each face a long-term water shortage. Over-pumped groundwater reserves and a federal mandate to reduce intake from streams and rivers to protect fish habitat require the two agencies to improve conservation and develop new supply sources."
            study["solution"]="Civinomics interviewed more than 1,500 residents using iPads to determine base-level awareness of the shortage and get feedback on potential solutions, including conservation and desalination."
            study["results"]="Respondents were enthusiastic about conservation, and 20% signed up for a free home water efficiency audit. Seventy-five percent said that they supported continued study of desalination, but indicated that they would need more information to be sure. Slightly less than 20% (283) of all respondents signed up for continued agency updates on the issue."
            study["nextSteps"]="Civinomics will host an online workshop enabling the community to suggest and refine potential solutions to the region's water shortage. Additional public outreach will take place after the Environmental Impact Report for a regional desalination plant is completed, at which point comprehensive discussion of all options will be possible."
            study['respondents'] = 1538
            study['clientLogo']='soquelCreek.gif'
            study['clientName']='Soquel Creek Water District'


            partners=[]
            partner={}
            partner['name']="Santa Cruz Water District"
            partner['url']="http://www.cityofsantacruz.com/index.aspx?page=54"
            partners.append(partner)
            partner={}
            partner['name']="Soquel Creek Water District"
            partner['url']="http://www.soquelcreekwater.org/"
            partners.append(partner)
            study["partners"]=partners

            sponsors=[]
            study["sponsors"]=sponsors
            
            publications=[]
            publication={}
            publication['name']="New Ways to Engage the Community (WaterReuse CA, Annual Conference)"
            publication['url']="WateReuse_Technical_Paper_ipad.pdf"
            publications.append(publication)
            study["publications"]=publications
            
            pictures=[]
            picture={}
            picture['image']="scwd2_1.jpg"
            picture['title']="Oct. 7th, 2011"
            picture['caption']="Civinomics CMO Robert Singleton pilots the survey on Soquel Creek Residents at Safeway in Aptos, CA."
            pictures.append(picture)
            picture={}
            picture['image']="scwd2_2.jpg"
            picture['title']="Oct. 7th, 2011"
            picture['caption']="Robert Singleton and outreach representative Sami Mzali interviewing."
            pictures.append(picture)
            picture={}
            picture['image']="scwd2_3.png"
            picture['title']="Oct. 7th, 2011"
            picture['caption']="Robert and Sami pose for the camera."
            pictures.append(picture)
            picture={}
            picture['image']="scwd2_4.jpg"
            picture['title']="Oct. 8th, 2011"
            picture['caption']="Sami Mzali at the Cabrillo Farmers Market, Soquel, CA."
            pictures.append(picture)
            picture={}
            picture['image']="scwd2_5.jpg"
            picture['title']="Oct. 8th, 2011"
            picture['caption']="Robert Singleton at New Leaf Market, Santa Cruz, CA."
            pictures.append(picture)
            picture={}
            picture['image']="scwd2_6.jpg"
            picture['title']="Oct. 20th, 2011"
            picture['caption']="Outreach representatives Sami Mzali and Sarah Ragland at New Leaf Market, Santa Cruz, CA."
            pictures.append(picture)
            picture={}
            picture['image']="scwd2_10.png"
            picture['title']="Nov. 19th, 2011"
            picture['caption']="Rosalie Gordon at New Leaf Market, Santa Cruz, CA."
            pictures.append(picture)
            picture={}
            picture['image']="scwd2_11.png"
            picture['title']="Nov. 19th, 2011"
            picture['caption']="Survey respondents at New Leaf Market, Santa Cruz, CA."
            pictures.append(picture)
            picture={}
            picture['image']="scwd2_8.jpg"
            picture['title']="Mar. 2nd, 2012"
            picture['caption']="Manu Koenig, Civinomics CEO, interviews two UCSC students at Cruzio during First Friday, Santa Cruz, CA."
            pictures.append(picture)
            picture={}
            picture['image']="scwd2_9.jpg"
            picture['title']="Mar. 2nd, 2012"
            picture['caption']="Manu Koenig at Cruzio during First Friday, Santa Cruz, CA."
            pictures.append(picture)
            picture={}
            picture['image']="scwd2_7.jpg"
            picture['title']="Mar. 25th, 2012"
            picture['caption']="Robert Singleton presents project findings with Melanie Schumacher from the Soquel Creek Water District, WaterReuse California, Sacramento, CA."
            pictures.append(picture)
            study["pictures"]=pictures
            
            questions=[]
            question={}
            question['image']="conservation_types.png"
            question['title']="Question 6: Would you seriously consider implementing any of the following conservation measures in your own home?"
            questions.append(question)
            question={}
            question['image']="water_audit.png"
            question['title']="Question 7: Would you like a free home water efficiency audit?"
            questions.append(question)
            question={}
            question['image']="desal.png"
            question['title']="Question 8: Should we continue to study the environmental impact of desalination to meet our future water needs?"
            questions.append(question)
            study["questions"]=questions
            
        elif casestudyname=="landtrust":
            study["url"]="landtrust"
            study["title"]="Campaign for 10,000 Acres"
            study["image"]="landTrust.png"
            study["statusType"]="important"
            study["statusMessage"]="Closed"
            study["date"]="6-20-2012"
            study["background"]="The Land Trust of Santa Cruz County completed its Conservation Blueprint at the beginning of 2012. This document outlines the most important land in the county to protect based on biodiversity, irreplaceable water resources, and greatest risk for development. The Land Trust currently has the opportunity to acquire the first two major parcels outlined in the Blueprint, CEMEX Redwoods and Star Creek Ranch, and it needs to raise public awareness to get local residents involved in securing these acquisitions."
            study["solution"]="In a pilot outreach campaign, Civinomics interviewed 500 residents using iPads to raise awareness about the Conservation Blueprint and get public input on the managing documents for the new parcels. The outreach did not include fundraising and was purely educational in nature."
            study["results"]="Almost all (98%) of respondents indicated that protecting open space in Santa Cruz County is important to them, with 67% indicating that it is very important. As proof of this, 47% of all respondents opted in with a home address or email address to continue to follow the Land Trust."
            study["nextSteps"]="Civinomics will host an online workshop enabling the community to suggest edits to the new parcels' Conservation Easements - the managing documents for these pieces of conservation land."
            study["videoURL"]="http://player.vimeo.com/video/42731448"
            study['respondents'] = 500
            study['clientLogo']='landTrustLogo.jpg'
            study['clientName']='Land Trust of Santa Cruz County'


            partners=[]
            partner={}
            partner['name']="The Land Trust of Santa Cruz County"
            partner['url']="http://www.landtrustsantacruz.org/"
            partners.append(partner)
            study["partners"]=partners

            sponsors=[]
            study["sponsors"]=sponsors
            
            publications=[]
            study["publications"]=publications

            pictures=[]
            study["pictures"]=pictures
            
            questions=[]
            question={}
            question['image']="land_important1.png"
            question['title']="Question 3: How important to you is protecting open space in Santa Cruz County?"
            questions.append(question)
            question={}
            question['image']="suggestions.png"
            question['title']="Question 4: How can we increase use and appreciation of new conservation land?"
            questions.append(question)
            question={}
            question['image']="optins.png"
            question['title']="Question 6: Would you like to receive occasional updates from the Santa Cruz Land Trust?"
            questions.append(question)
            study["questions"]=questions

            c.video='<iframe src="http://player.vimeo.com/video/42731448" width="500" height="375" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>'
            
           

        elif casestudyname=="cap2":
            study["url"]="cap2"
            study["title"]="Santa Cruz Climate Action Plan"
            study["image"]="CAP.png"
            study["statusType"]="important"
            study["statusMessage"]="Closed"
            study['respondents'] = 500
            study['clientLogo']='scCAP.jpg'
            study['clientName']='City of Santa Cruz Climate Action Plan'
            study['sponsorLogo']='allterraSolar.jpg'
            study['sponsorName']='Allterra Solar'
            study["date"]="9-1-12"
            study["background"]="The Santa Cruz Climate Action Plan was officially adopted by the Santa Cruz City Council in June 2012 - but with no money available for implementation or marketing, it didn't look likely to change things anytime soon. While the plan lays out a detailed roadmap to increase bike commuting and residential solar, it can't possibly have an effect if people aren't aware that it exists."
            study["solution"]="Civinomics worked with the City's Climate Action Coordinator, Ross Clark, to design an outreach survey funded by local sustainable businesses. The pilot project set out to prove that: 1) the City could raise awareness about its Climate Action Plan without spending city money; 2) City residents would be interested in participating; and 3) Civinomics could help develop public policy that would allow the City to reach its emissions reduction targets."
            study["results"]="Civinomics conducted 500 interviews with Santa Cruz residents. Allterra Solar, a Santa Cruz-based solar installer, sponsored the outreach. The study revealed that 80% of residents had NOT heard about the Climate Action Plan, suggesting that more awareness programs are needed. Nevertheless, 65% of respondents were willing to pay between $1 and $5 per month to see the Climate Action Plan implemented. Civinomics specifically polled about Community Choice Aggregation - a new mechanism that allows counties or cities to create a regional power authority to buy and sell local renewable energy. It found that 90% of respondents would support such a program."
            study["nextSteps"]="With demonstrable support and a proven, community business-funded outreach model, the City of Santa Cruz can proceed to develop policies such as a Climate Action Plan-related tax, Community Choice Aggregation and others."
            
            partners=[]
            partner={}
            partner['name']="City of Santa Cruz, Climate Action Plan"
            partner['url']="http://www.cityofsantacruz.com/index.aspx?page=1544"
            partners.append(partner)
            study["partners"]=partners

            sponsors=[]
            sponsor={}
            sponsor['name']="Allterra Solar"
            sponsor['url']="http://www.allterrasolar.com/"
            sponsors.append(sponsor)
            study["sponsors"]=sponsors
            
            publications=[]
            publication={}
            publication['name']="Climate Action Plan Survey - Final Report"
            publication['url']="CAP_PublicReport_091112.pdf"
            publications.append(publication)
            study["publications"]=publications

            pictures=[]
            picture={}
            picture['image']="IMG_1.JPG"
            picture['title']="April 21st, 2012 - Earthday Festival, San Lorenzo Park, Santa Cruz, CA"
            picture['caption']="Aaron White conducts the first interview of the day."
            pictures.append(picture)
            picture={}
            picture['image']="IMG_2.JPG"
            picture['title']="April 21st, 2012 - Earthday Festival, San Lorenzo Park, Santa Cruz, CA"
            picture['caption']="Robert Singleton talks to two UCSC students."
            pictures.append(picture)
            picture={}
            picture['image']="IMG_3.JPG"
            picture['title']="April 21st, 2012 - Earthday Festival, San Lorenzo Park, Santa Cruz, CA"
            picture['caption']="The UCSC Sustainability Tent"
            pictures.append(picture)
            picture['image']="IMG_4.jpg"
            picture['title']="April 21st, 2012 - Earthday Festival, San Lorenzo Park, Santa Cruz, CA"
            picture['caption']="Marhsall Comden speaks to a festive participant"
            pictures.append(picture)
            picture={}
            picture['image']="IMG_5.JPG"
            picture['title']="April 21st, 2012 - Earthday Festival, San Lorenzo Park, Santa Cruz, CA"
            picture['caption']="Overview of the Festival Grounds"
            pictures.append(picture)
            picture={}
            picture['image']="IMG_6.JPG"
            picture['title']="April 21st, 2012 - Earthday Festival, San Lorenzo Park, Santa Cruz, CA"
            picture['caption']="Manu Koenig engages a resident who stopping by the Civinomics table."
            pictures.append(picture)
            picture={}
            picture['image']="IMG_7.JPG"
            picture['title']="April 21st, 2012 - Earthday Festival, San Lorenzo Park, Santa Cruz, CA"
            picture['caption']="Interview complete, Manu happily enters a few last pieces of information."
            pictures.append(picture)
            picture={}
            picture['image']="IMG_8.JPG"
            picture['title']="April 21st, 2012 - Earthday Festival, San Lorenzo Park, Santa Cruz, CA"
            picture['caption']="A survey respondent receives a sticker for her participation."
            pictures.append(picture)
            picture={}
            picture['image']="IMG_9.JPG"
            picture['title']="April 21st, 2012 - Earthday Festival, San Lorenzo Park, Santa Cruz, CA"
            picture['caption']="Aaron and a Prop 37 canvasser exchange smiles and informaiton."
            pictures.append(picture)
            study["pictures"]=pictures
            
            questions=[]
            question={}
            question['image']="question_heardCAP.jpeg"
            question['title']="Question 1: Have you heard of the Santa Cruz Climate Action Plan?"
            questions.append(question)
            question={}
            question['image']="question_pay.jpeg"
            question['title']="Question 3: How much would you be willing to pay per month to see the Climate Action Plan implemented? (answers in $ amount)"
            questions.append(question)
            question={}
            question['image']="question_supportCCA.jpeg"
            question['title']="Question 6: How likely are you to support Community Choice Aggregation in Santa Cruz? (0 = not at all likely, 100 = very likely)"
            questions.append(question)
            study["questions"]=questions


        elif casestudyname =="eastsideProject":
            study["url"]="eastsideProject"
            study["title"]="Eastside Recycled Water Project"
            study["image"]="eastsideProject.png"
            study["statusType"]="success"
            study["statusMessage"]="Open"
            study["respondents"]="934"
            study["date"]="6-24-2012"
            study["background"]="The San Francisco Public Utilities Commission (SFPUC) has a goal to provide 4 million gallons per day of recycled water to the City of San Francisco. In order to reach this goal it is building three new recycled water facilities, including one serving Golden Gate Park and one serving the City's downtown, or 'Eastside.' Before selecting a location for the Eastside facility, the SFPUC wants to collect substantial public input. However, it has proven extremely difficult to get the public to show up to in-person forums and workshops."
            study["solution"]="Civinomics created an iPad survey for use in street outreach that discusses the basic principles behind recycled water and its use in San Francisco. The survey then presents each of the potential facility sites, asking respondents to indicate which they prefer, which they oppose and what comments they wish to make. Respondents also supply feedback on whether they prefer a minimal facility or one that includes community space or recreational amenities."
            study["results"]="With Civinomics' help, the SFPUC has been able to collect substantially more public input than ever before. The iPad survey is particularly effective for reaching residents in affected neighborhoods where household access to personal computers or the internet is not a given. Results will be published upon completion of the outreach."
            study["nextSteps"]=""

            study['clientLogo']='sfpucLogo.png'
            study['clientName']='San Francisco Public Utilities Commission'

            partners=[]
            partner={}
            partner['name']="San Francisco Public Utilities Commission"
            partner['url']="http://sfwater.org/bids/projectDetail.aspx?prj_id=311"
            partners.append(partner)
            study["partners"]=partners

            sponsors=[]
            study["sponsors"]=sponsors

            publications=[]
            study["publications"]=publications

            pictures=[]
            picture={}
            picture['image']="IMG_001.jpg"
            picture['title']="June, 2012 - Ferry Building, San Francisco, CA"
            picture['caption']="Robert Singleton and Derrold Purifoy trade free t-shirts for surveys."
            pictures.append(picture)
            picture={}
            picture['image']="IMG_002.jpg"
            picture['title']="June, 2012 - Ferry Building, San Francisco, CA"
            picture['caption']="A survey respondent shows off his new sticker for the camera."
            pictures.append(picture)
            picture={}
            picture['image']="IMG_003.jpg"
            picture['title']="August, 2012 - Dolores Park, San Francisco, CA"
            picture['caption']="AJ Burleson leads a group of park-goers through the survey."
            pictures.append(picture)
            picture={}
            picture['image']="IMG_004.jpg"
            picture['title']="September, 2012 - Portola Garden Tour"
            picture['caption']="A happy respondent shows off the iPad survey."
            pictures.append(picture)
            picture={}
            picture['image']="IMG_005.jpg"
            picture['title']="September, 2012 - Portola Garden Tour"
            picture['caption']="AJ Burleson explains the details of the proposed facility."
            pictures.append(picture)
            picture={}
            picture['image']="IMG_006.jpg"
            picture['title']="September, 2012 - Portola Garden Tour"
            picture['caption']="Two respondents contemplating their preferences for a facility site."
            pictures.append(picture)
            picture={}
            picture['image']="IMG_007.jpg"
            picture['title']="September, 2012 - Portola Garden Tour"
            picture['caption']="SF resident smiles in the midst of reviewing the plans."
            pictures.append(picture)
            study["pictures"]=pictures

            questions=[]
            study["questions"]=questions

        elif casestudyname =="SSIP":
            study["url"]="SSIP"
            study["title"]="Sewer System Improvement Program"
            study["image"]="ssipCover.png"
            study["statusType"]="success"
            study["statusMessage"]="Open"
            study["respondents"]="1200"
            study["date"]=" 11-25-2012"
            study["background"]="The San Francisco Public Utilities Commission (SFPUC) is undertaking the multi-billion-dollar Sewer System Improvement Program (SSIP) to modernize the City's infrastructure and ensure the system functions in the event of a major earthquake. These improvements require construction in every neighborhood of the City as well as significant rate increases for residents. A substantial amount of public input is required before and during the project, however, it has proven historically difficult to get the public to show up for in-person forums and workshops."
            study["solution"]="Civinomics created an iPad survey for use in street outreach that provides residents an overview of the SSIP and gauges their support for its different elements. Respondents report sewer related problems, indicate their priorities for the overall project (minimizing costs, reducing odors, creating jobs, etc.) and indicate what they believe to be a reasonable rate increase to cover the cost of the improvements. The surveys are being conducted in the eight watersheds throughout the city."
            study["results"]="Results will be published upon completion of the outreach."
            study["nextSteps"]=""

            study['clientLogo']='sfpucLogo.png'
            study['clientName']='San Francisco Public Utilities Commission'

            partners=[]
            partner={}
            partner['name']="San Francisco Public Utilities Commission"
            partner['url']="http://sfwater.org/bids/projectDetail.aspx?prj_id=311"
            partners.append(partner)
            study["partners"]=partners

            sponsors=[]
            study["sponsors"]=sponsors

            publications=[]
            study["publications"]=publications

            pictures=[]
            study["pictures"]=pictures

            questions=[]
            study["questions"]=questions

            c.video='<iframe width="560" height="315" src="http://www.youtube.com/embed/m4039IQU7BM" frameborder="0" allowfullscreen></iframe></p>'


        elif casestudyname =="techCommuter":
            study["url"]="techCommuter"
            study["title"]="Santa Cruz Tech Commuter Survey"
            study["image"]="techCommuter.png"
            study["statusType"]="danger"
            study["statusMessage"]="Closed"
            study["date"]=" 3-25-2014"
            study["background"]="The San Francisco Public Utilities Commission (SFPUC) is undertaking the multi-billion-dollar Sewer System Improvement Program (SSIP) to modernize the City's infrastructure and ensure the system functions in the event of a major earthquake. These improvements require construction in every neighborhood of the City as well as significant rate increases for residents. A substantial amount of public input is required before and during the project, however, it has proven historically difficult to get the public to show up for in-person forums and workshops."
            study["solution"]="Civinomics created an iPad survey for use in street outreach that provides residents an overview of the SSIP and gauges their support for its different elements. Respondents report sewer related problems, indicate their priorities for the overall project (minimizing costs, reducing odors, creating jobs, etc.) and indicate what they believe to be a reasonable rate increase to cover the cost of the improvements. The surveys are being conducted in the eight watersheds throughout the city."
            study["results"]=""
            study["pressRelease"]='techCommuters'
            study["nextSteps"]=""
            study['stats']='dcCommuterSurvey'

            study['respondents'] = 102
            study['partnerLogo']='ssvLogo.png'
            study['partnerName']='South Swell Ventures'
            study['scope'] = ''
            study['tag'] = ''

            partners=[]
            partner={}
            partner['name']="South Swell Ventures"
            partner['url']="http://sfwater.org/bids/projectDetail.aspx?prj_id=311"
            partners.append(partner)
            study["partners"]=partners

            sponsors=[]
            study["sponsors"]=sponsors

            publications=[]
            study["publications"]=publications

            pictures=[]
            study["pictures"]=pictures

            questions=[]
            study["questions"]=questions

        elif casestudyname =="dmc":
            study["url"]="dmc"
            study["title"]="Downtown Management Corporation - Customer Feedback Survey"
            study["image"]="hostPic.png"
            study["statusType"]="danger"
            study["statusMessage"]="Closed"
            study["date"]=" 4-9-2014"
            study["background"]="Downtown SC is gnarly, we asked how the help's doing."
            study["solution"]="Civinomics created an iPad survey for use in street outreach that.."
            study["results"]=""
            study["pressRelease"]='dmc'
            study["nextSteps"]=""
            study['stats']='dcDmcSurvey'
            study['link']= 'http://surveys.civinomics.com/dmc'
            study["text"]='dmc'

            study['respondents'] = 183
            study['clientLogo']='dmcLogo.png'
            study['clientName']='Downtown Management Corporation'
            study['scope'] = ''
            study['tag'] = ''

            partners=[]
            partner={}
            partner['name']="Boss DMC"
            partner['url']="http://www.civ.io"
            partners.append(partner)
            study["partners"]=partners

            sponsors=[]
            study["sponsors"]=sponsors

            publications=[]
            study["publications"]=publications

            pictures=[]
            study["pictures"]=pictures

            questions=[]
            study["questions"]=questions

        elif casestudyname =="svbagban":
            study["url"]="svbagban"
            study["title"]="Scotts Valley Plastic Bag Ban Opinion Poll"
            study["image"]="bagCreek.jpg"
            study["statusType"]="danger"
            study["statusMessage"]="Closed"
            study["date"]=" 4-8-2014"
            study["background"]="Plastic Bags are bad."
            study["solution"]="Plastic Bag Fees ain't so bad."
            study["results"]=""
            study["text"]='svBagBan'
            study["nextSteps"]=""
            study['stats']='plasticBagBan'
            study['link']= 'http://surveys.civinomics.com/svbagban'

            study['respondents'] = 397
            study['partnerLogo']='sosLogo.jpg'
            study['partnerName']='Save Our Shores'
            study['scope'] = ''
            study['tag'] = ''

            partners=[]
            partner={}
            partner['name']="Boss plasticBagBan"
            partner['url']="http://www.civ.io"
            partners.append(partner)
            study["partners"]=partners

            sponsors=[]
            study["sponsors"]=sponsors

            publications=[]
            study["publications"]=publications

            pictures=[]
            study["pictures"]=pictures

            questions=[]
            study["questions"]=questions
            
            
            


        return render("/derived/corp_casestudy.bootstrap")


    def displayCareer(self, id):
        careername=id
        career={}
        if careername=="engfrontend":
            career["title"]="Software Engineer - Front End"
            career["commitment location"]="Fulltime - Santa Cruz, CA"
            career["description"]="Make this site beautiful. We need someone who is going to transform Civinomics into a clean, modern web app. Doing so will require more than a few photoshop mockups. Ideally you have already used bootstrap, angular JS and know some python. You can't make the front end fun unless you know the basics of passing data around. Show us that you know way more than us about composing clean, snappy CSS. If you have experience with iOS to boot, that rocks."

            requirements=[]
            requirement = "Flat design expertise"
            requirements.append(requirement)
            requirement = "bootstrap"
            requirements.append(requirement)
            requirement = "angular JS or similar javascript MVC framework"
            requirements.append(requirement)
            requirement = "Javascript and jQuery"
            requirements.append(requirement)
            requirement = "CSS"
            requirements.append(requirement)
            requirement = "HTML"
            requirements.append(requirement)
            requirement = "Able to work with a small team and quickly adapt"
            requirements.append(requirement)
            career["requirements"]=requirements

            recommendeds=[]
            recommended = "python"
            recommendeds.append(recommended)
            recommended = "iOS"
            recommendeds.append(recommended)
            career["recommendeds"]=recommendeds

        if careername=="engbackend":
            career["title"]="Software Engineer - Back End"
            career["commitment location"]="Fulltime - Santa Cruz, CA"
            career["description"]="Make Civinomics faster, more secure and self-sustaining. We're looking for someone who can help us quickly materialize revenue opportunities on the platform, refine our architecture, internationalize and scale. Experience managing a team is a huge plus."

            requirements=[]
            requirement = "Comfortable in a *nix environment"
            requirements.append(requirement)
            requirement = "Python 2.X"
            requirements.append(requirement)
            requirement = "MySQL"
            requirements.append(requirement)
            requirement = "SQLAlchemy"
            requirements.append(requirement)
            requirement = "angular JS or similar javascript MVC framework"
            requirements.append(requirement)
            requirement = "Javascript and jQuery"
            requirements.append(requirement)
            requirement = "CSS"
            requirements.append(requirement)
            requirement = "HTML"
            requirements.append(requirement)
            requirement = "An eye for detail"
            requirements.append(requirement)
            requirement = "Chooses to write maintainable code instead of brute-force or clever code, every time"
            requirements.append(requirement)
            career["requirements"]=requirements

            recommendeds=[]
            recommended = "Experience working with open schemas"
            recommendeds.append(recommended)
            recommended = "Experience with scaling applications and databases"
            recommendeds.append(recommended)
            recommended = "Experience with the Pylons or Pyramid framework"
            recommendeds.append(recommended)
            recommended = "Proven ability to lead a development team"
            recommendeds.append(recommended)
            career["recommendeds"]=recommendeds

        if careername=="prgmManager":
            career["title"]="Program Manager"
            career["commitment location"]="Fulll time - Santa Cruz, CA"
            career["description"]="Implement best practices to help Civinomics customers get the most out of their usage. Make vital product recommendations based on customer feedback. Facilitate cutting edge online interaction paradigm."

            requirements=[]
            requirement = "Clear and Effective Communication"
            requirements.append(requirement)
            requirement = "Scientific approach to observation, must not let subjective opinions color recommendations"
            requirements.append(requirement)
            requirement = "Patience and respect for customers and team mates"
            requirements.append(requirement)
            career["requirements"]=requirements

            recommendeds=[]
            career["recommendeds"]=recommendeds


        if careername=="prep":
            career["title"]="Public Outreach Representative"
            career["commitment location"]="Part time - Santa Cruz and San Francisco, CA"
            career["description"]="Person-to-person interaction is still the most effective means of community engagement, that's why we decided to re-invent the practice for the 21st century. We conduct face-to-face interviews for public agencies and non-profits via iPad. We are looking to hire new field organizers for the purposes of conducting surveys both at community events and through door-to-door outreach. We do not fundraise - our campaigns are educational and research oriented. Previous experience is recommended, but not required. Community Representatives are paid $3.00 - $7.00 per interview with an additional $2 for interviews conducted in a foreign language. Most representatives complete between 4-8 interviews per hour. We are looking to fill these positions ASAP."

            requirements=[]
            requirement = "Clear, effective communication skills"
            requirements.append(requirement)
            requirement = "Cultural competency"
            requirements.append(requirement)
            requirement = "The ability memorize facts and become an expert about issues"
            requirements.append(requirement)
            career["requirements"]=requirements

            recommendeds=[]
            career["recommendeds"]=recommendeds

        if careername=="acctManager":
            career["title"]="Account Manager"
            career["commitment location"]="Full time - Santa Cruz and San Francisco, CA"
            career["description"]="We need a meticulous go getter who can keep clients happy and grow business. Existing clients range from government, to non-profit organizations, to political candidates, to sponsors.  Demonstrated passion for social causes through previous work or serious personal projects is a must. Amazing talent with CRM and PowerPoint / Keynote required. Prove to us that you can listen to what a client needs and work with a team to over-deliver on tight deadlines."

            requirements=[]
            requirement = "Experience and comfort with responsibility"
            requirements.append(requirement)
            requirement = "PowerPoint / Keynote Mastery"
            requirements.append(requirement)
            requirement = "Proven ability to make lasting client relationships"
            requirements.append(requirement)
            requirement = "Experience in Hightech"
            requirements.append(requirement)
            requirement = "Passion for citizenship and social justice"
            requirements.append(requirement)
            career["requirements"]=requirements

            recommendeds=[]
            career["recommendeds"]=recommendeds

        c.career=career   
        c.pagetype="careers"  
        c.title="Careers"
        return render("/derived/corp_career.bootstrap")


    def careers(self):
        c.careers=[]
        engfrontend={}
        engfrontend["title"]="Software Engineer - Front End"
        engfrontend["department"]="Engineering"
        engfrontend["url"]="engfrontend"
        c.careers.append(engfrontend)
        engbackend={}
        engbackend["title"]="Software Engineer - Back End"
        engbackend["department"]="Engineering"
        engbackend["url"]="engbackend"
        c.careers.append(engbackend)
        career={}
        #career["title"]="Program Manager"
        #career["department"]="Operations"
        #career["url"]="prgmManager"
        #c.careers.append(career)
        career["title"]="Account Manager"
        career["department"]="Sales"
        career["url"]="acctManager"
        c.careers.append(career)
        prep={}
        prep["title"]="Public Outreach Representative"
        prep["department"]="Outreach"
        prep["url"]="prep"
        c.careers.append(prep)

        c.title = 'Careers'
        c.pagetype="careers" 
        return render('/derived/corp_listCareers.bootstrap')


    def team(self):
        c.title = 'Team'
        c.pagetype="team" 

        c.team=[]
        toddAnderson={}
        toddAnderson["name"]="Todd Anderson"
        toddAnderson['title']='Lead Mobile Engineer'
        toddAnderson['bio']="Todd Anderson has experience working in the crowd-sourced web-app sphere. His interests include game theory, radical UI, mobile integration and empowering communities. An avid surfer, Todd is excited to empower the global surf community with Civinomics' platform."
        toddAnderson['photo']='todd_585.jpg'
        toddAnderson['photoHover']='todd_silly_585.jpg'
        c.team.append(toddAnderson)
        kelseyG={}
        kelseyG["name"]="Kelsey Grimsley"
        kelseyG['title']='Outreach Representative'
        kelseyG['bio']="Kelsey gained valuable experience with diverse constituents as Congressman Henry Waxman's intern for his D.C. office (summer, 2012) and for Congressman Sam Farr in his local Santa Cruz office (spring, 2013). She campaigned in three states for Obama for America (2012), and helped coordinate successful regional environmental campaigns including Ban-the-Bag in Santa Cruz, CA. "
        kelseyG['photo']='kelsey_grimsley_585.jpg'
        kelseyG['photoHover']='kelsey_grimsley_585.jpg'
        c.team.append(kelseyG)
        estherKim={}
        estherKim["name"]="Esther Kim"
        estherKim['title']='Marketing Manager'
        estherKim['bio']="My name is Esther Kim, I'm a recent graduate from UCSC in Business Management & Economics. I am an avid blogger, amateur videographer, and a work hard play hard advocate. I fell in love with Santa Cruz when I started surfing and mountain biking and I don't plan on leaving anytime soon. At Civinomics, I hope to bring in a specialized skillset of what I call 'grassroots' marketing to help set a structured brand goal of being a community leader."
        estherKim['photo']='esther_585.jpg'
        estherKim['photoHover']='esther_silly_585.jpg'
        c.team.append(estherKim)
        manuK={}
        manuK["name"]="Manu Koenig"
        manuK['title']='Founder & CEO'
        manuK['bio']="Manu makes sure Civinomics runs on time. Previously he was General Manager of Strategic Partnerships at Martini Media Network - a Venrock backed vertical ad network. There he also served as Operations Manager, running campaigns for clients including Lexus, Chanel, and British Air. Manu holds dual US-European citizenship and worked as a Corporate Campaign Intern for Deutsche Bahn AG in Berlin. He studied German and Management Science at Stanford."
        manuK['photo']='manu_585.jpg'
        manuK['photoHover']='manu_silly_585.jpg'
        c.team.append(manuK)
        chrisN={}
        chrisN["name"]="Chris Neklason"
        chrisN['title']='Product Management'
        chrisN['bio']="Chris Neklason has been involved with community networking since 1984, before the Internet, and has decades of experience as a UNIX software engineer and as co-founder of Cruzio, one of the oldest ongoing independent ISPs in the United States."
        chrisN['photo']='chris_585.jpg'
        chrisN['photoHover']='chris_silly_585.jpg'
        c.team.append(chrisN)
        derroldP={}
        derroldP["name"]="Derrold Purifoy"
        derroldP['title']='Public Outreach Manager'
        derroldP['bio']="Derrold was born in Orange, Texas and has lived his adult life in San Francisco. His business experience includes working in Customer Service, B2B Sales and Marketing Research. His hobbies include movies, literature and photography. He's excited to work on projects that have a positive impact on the community."
        derroldP['photo']='derrold_purifoy.jpg'
        derroldP['photoHover']='derrold_purifoy.jpg'
        c.team.append(derroldP)
        robertS={}
        robertS["name"]="Robert Singleton"
        robertS['title']='Founder & CMO'
        robertS['bio']="Robert is the political domain expert and charismatic brand manager for Civinomics. He has extensive experience as a community organizer and in public relations, having worked on over a dozen political campaigns in Sonoma and Santa Cruz Counties, including the SMART commuter train, urban sprawl and growth boundary ordinances, candidates for state assembly, and key city positions. He recently graduated from UCSC with a degree in Politics."
        robertS['photo']='robert_585.jpg'
        robertS['photoHover']='robert_silly_585.jpg'
        c.team.append(robertS)
        russellSterten={}
        russellSterten["name"]="Russell Sterten"
        russellSterten['title']='Program Manager '
        russellSterten['bio']="Hi, my name is Russell and it's good to be on board with Civinomics.  I am excited about the prospect of leveraging cutting edge communications and Web 2.0 technologies to dramatically increase people's engagement on issues facing their community. Before joining Civinomics I worked as a grassroots campaign organizer - most recently on a San Rafael city councilman's successful bid for the State Assembly - and have also been a substitute teacher in the East Bay and Marin.  Now I am looking forward to working with Civinomics and empowering people to help change the world."
        russellSterten['photo']='russell_585.jpg'
        russellSterten['photoHover']='russell_silly_585.jpg'
        c.team.append(russellSterten)

        c.advisors=[]

        fredK={}
        fredK["name"]="Fred Keeley"
        fredK['title']='Political Strategy'
        fredK['bio']= "Fred Keeley is treasurer of Santa Cruz County, a position he has held since January 2005. He served in the California State Assembly from 1996 to 2002 and served four years as the Speaker pro Tempore of the Assembly. During the California energy crisis in 2000 and 2001, Speaker Robert Hertzberg appointed Mr. Keeley chief operating officer for the Assembly on the energy crisis. In that capacity, Mr. Keeley authored California's solution to the energy crisis. He also helped in forging budget compromises between Democrats and Republicans in the Legislature."
        fredK['photo']='fred_keeley_585.jpg'
        fredK['photoHover']='fred_keeley_585.jpg'
        c.advisors.append(fredK)

        edolfoG={}
        edolfoG["name"]="Edolfo Garza-Licudine"
        edolfoG['title']='Technichal Cofounder'
        edolfoG['bio']="Edolfo has 10 years experience programming and 2 years experience managing databases and working in a biophysics research team. He graduated from UCSC with degrees in Applied Physics and Computational Mathematics in 2010."
        edolfoG['photo']='edolfo_garzalicudine.jpg'
        edolfoG['photoHover']='edolfo_garzalicudine.jpg'
        c.advisors.append(edolfoG)

        lloydT={}
        lloydT["name"]="Lloyd Tabb"
        lloydT['title']='Technology'
        lloydT['bio']="Lloyd has been a technology revolutionary for 25 years, driving important trends in how the world uses the Internet. Originally a database and languages architect at Borland International, Lloyd left Borland to found Commerce Tools, where he wrote the first application server for the web. After Commerce Tools was acquired by Netscape in 1995, Lloyd was Principal Engineer on Netscape Navigator Gold, led several releases of Communicator, and helped define the creation of Mozilla.org. As CTO of LiveOps, the first commercial crowd-sourced company, he designed the crowd-sourced ecosystem. Lloyd was also a co-founder of Readyforce and advisor to Luminate. He is currently Founder, Chairman and CTO of Looker."
        lloydT['photo']='lloyd_tabb.jpg'
        lloydT['photoHover']='lloyd_tabb.jpg'
        c.advisors.append(lloydT)

        tomY={}
        tomY["name"]="Tom Yoritaka"
        tomY['title']='Products & Community Development'
        tomY['bio']= "Tom Yoritaka is a Senior Director & General Manager at Cisco Systems, Inc. He is also the Managing Director of Cisco Entrepreneurs in Residence - the company's innovation program for eary-stage start-ups. Prior to joining Cisco, he held various executive & leadershiop positions in Web techbology & product management at Yahoo! & Microsoft. He also worked as a strategy consultant at The Boston Consulting Group & McKenna Group. He holds a master's degree from Harvard University John F. Kennedy School of Government, an MBA from The University of Chicago Booth School of Business & an undergraduate degree from Northwestern University."
        tomY['photo']='tom_yoritaka.png'
        tomY['photoHover']='tom_yoritaka.png'
        c.advisors.append(tomY)

        return render('/derived/corp_team.bootstrap')

    def news(self):
        c.title = 'News'
        c.pagetype="news" 

        c.articles=[]
       
        article={}
        article['title']="Civinomics Rising"
        article['link']='http://www.gtweekly.com/index.php/santa-cruz-news/good-times-cover-stories/5265-civinomics-rising.html'
        article['date']='12.11.2013'
        article['source']='Good Times'
        c.articles.append(article)

        article={}
        article['title']="Dawn of Civinomicon"
        article['link']='http://www.gtweekly.com/index.php/santa-cruz-news/36-santa-cruz-business-news/5211-dawn-of-civinomicon.html'
        article['date']='11.20.2013'
        article['source']='Good Times'
        c.articles.append(article)

        article={}
        article['title']="Civinomics Looking for Pubic Input"
        article['link']='http://santacruz.patch.com/groups/announcements/p/civinomics-looking-for-pubic-input'
        article['date']='11.19.2013'
        article['source']='Santa Cruz Patch'
        c.articles.append(article)

        article={}
        article['title']="Santa Cruz hackathon brings new ideas to the political table"
        article['link']='http://www.santacruzsentinel.com/santacruz/ci_24544092/santa-cruz-hackathon-brings-new-ideas-political-table'
        article['date']='11.17.2013'
        article['source']='Santa Cruz Sentinel'
        c.articles.append(article)

        article={}
        article['title']="Civinomicon Seeks to Fix Public Discourse"
        article['link']='http://www.santacruz.com/news/2013/11/05/civinomicon_seeks_to_fix_local_public_discourse'
        article['date']='11.15.2013'
        article['source']='SantaCruz.com'
        c.articles.append(article)

        article={}
        article['title']="Community gathers to discuss downtown"
        article['link']='http://www.register-pajaronian.com/v2_news_articles.php?heading=0&page=72&story_id=15440'
        article['date']='11.08.2013'
        article['source']='Register Pajaronian'
        c.articles.append(article)
        article={}
        article['title']="Civinomicon Seeks to Fix Public Discourse"
        article['link']='http://www.santacruz.com/news/2013/11/05/civinomicon_seeks_to_fix_local_public_discourse'
        article['date']='11.05.2013'
        article['source']='Santa Cruz Weekly'
        c.articles.append(article)
        article={}
        article['title']="Tech startup Civinomics to host civic engagement conference"
        article['link']='http://www.register-pajaronian.com/v2_news_articles.php?heading=0&story_id=15366&page=72'
        article['date']='10.25.2013'
        article['source']='Register Pajaronian'
        c.articles.append(article)
        article={}
        article['title']="KSCO Presents Ethan Bearman October 3, 2013. In-studio with Robert Singleton, Founder and CMO of Civinomics"
        article['link']='http://podcast.ethanbearman.com/ksco-presents-ethan-bearman-october-3-2013/'
        article['date']='10.03.2013'
        article['source']='KSCO'
        c.articles.append(article)
        article={}
        article['title']="(Video) KSCO Presents Ethan Bearman October 3, 2013. In-studio with Robert Singleton, Founder and CMO of Civinomics"
        article['link']='http://www.youtube.com/watch?v=VfXiMWpUBZ8&feature=youtu.be'
        article['date']='10.03.2013'
        article['source']='YouTube'
        c.articles.append(article)
        article={}
        article['title']="Lack of eatery, entertainment options top downtown Watsonville survey"
        article['link']='http://www.register-pajaronian.com/v2_news_articles.php?heading=0&page=72&story_id=15248'
        article['date']='10.03.2013'
        article['source']='Register Pajaronian'
        c.articles.append(article)
        article={}
        article['title']="Survey: Watsonville downtown needs more restaurants, shops, entertainment: Downtown vision project seeks to engage public"
        article['link']='http://www.santacruzsentinel.com/watsonville/ci_24226760/survey-watsonville-downtown-needs-more-restaurants-shops-entertainment'
        article['date']='10.02.2013'
        article['source']='Santa Cruz Sentinel'
        c.articles.append(article)
        article={}
        article['title']="Get Stoked on Social. Santa Cruzs Best Twitter Accounts"
        article['link']='http://santacruzlife.com/get-stoked-social-santa-cruzs-best-twitter-accounts/'
        article['date']='9.30.2013'
        article['source']='SantaCruzLife.com'
        c.articles.append(article)
        article={}
        article['title']="The Civinomics blog on civic discourse"
        article['link']='http://santacruznews.org/people/the-civinomics-blog-on-civic-discourse/'
        article['date']='9.30.2013'
        article['source']='SantaCruzNews.org'
        c.articles.append(article)
        article={}
        article['title']="Civinomics tackles Shakespeare, downtown Watsonville, plastic bags"
        article['link']='http://www.santacruzsentinel.com/santacruz/ci_24008994/civinomics-tackles-shakespeare-downtown-watsonville-plastic-bags?source=rss&utm_source=dlvr.it&utm_medium=twitter'
        article['date']='9.03.2013'
        article['source']='Santa Cruz Sentinel'
        c.articles.append(article)
        article={}
        article['title']="Building an Entrepreneurial Pipeline in Santa Cruz (Part 3)"
        article['link']='http://www.xconomy.com/san-francisco/2013/08/01/building-an-entrepreneurial-pipeline-in-santa-cruz/'
        article['date']='8.1.2013'
        article['source']='xconomy.com'
        c.articles.append(article)
        article={}
        article['title']="Seeding a New Generation of Startups in Santa Cruz (Part 2)"
        article['link']='http://www.xconomy.com/san-francisco/2013/07/31/seeding-a-new-generation-of-startups-in-santa-cruz/'
        article['date']='7.31.2013'
        article['source']='xconomy.com'
        c.articles.append(article)
        article={}
        article['title']="Santa Cruz, the City Over the Hill, Works to Build Its Own Startup Culture (Part 1)"
        article['link']='http://www.xconomy.com/san-francisco/2013/07/30/santa-cruz-the-city-over-the-hill-builds-its-own-startup-culture/'
        article['date']='7.30.2013'
        article['source']='xconomy.com'
        c.articles.append(article)
        article={}
        article['title']="BUSINESS DIGEST, JULY 20, 2013: CIVINOMICS INVITES ELECTED OFFICIALS"
        article['link']='http://www.contentboost.com/news/2013/07/19/7289426.htm'
        article['date']='7.19.2013'
        article['source']='xconomy.com'
        c.articles.append(article)
        article={}
        article['title']="Monterey County Herald publisher, advertising director add Santa Cruz Sentinel to duties Omernick, Powell fill roles at Santa Cruz Sentinel"
        article['link']='http://robertpowelldigitalfirst.wordpress.com/2013/06/29/monterey-county-herald-publisher-advertising-director-add-santa-cruz-sentinel-to-duties-omernick-powell-fill-roles-at-santa-cruz-sentinel/'
        article['date']='6.20.2013'
        article['source']='Robert Powell Blog'
        c.articles.append(article)
        article={}
        article['title']="Bring Your Own Bag"
        article['link']='http://www.gtweekly.com/index.php/santa-cruz-news/santa-cruz-environmental-news/4771-bring-your-own-bag.html'
        article['date']='5.07.2013'
        article['source']='Good Times'
        c.articles.append(article)
        article={}
        article['title']="Civinomics: A new kind of civic participation for the social media world"
        article['link']='http://santacruznews.org/people/civinomics-a-new-kind-of-civic-participation-for-the-social-media-world/'
        article['date']='4.12.2013'
        article['source']='SantaCruzNews.org'
        c.articles.append(article)
        article={}
        article['title']="Civinomics' ceremony attracts Santa Cruz leaders"
        article['link']='http://www.santacruzsentinel.com/localnews/ci_23008123/civinomics-ceremony-attracts-santa-cruz-leaders'
        article['date']='4.11.2013'
        article['source']='Santa Cruz Sentinel'
        c.articles.append(article)
        article={}
        article['title']="Civinomics to launch community workshops online, seeking public safety solutions"
        article['link']='http://www.santacruzsentinel.com/localnews/ci_22826816/civinomics-launch-community-workshops-online-seeking-public-safety'
        article['date']='3.19.2013'
        article['source']='Santa Cruz Sentinel'
        c.articles.append(article)
        article={}
        article['title']="Santa Cruz's Cruzio hosts open house Friday to showcase new businesses"
        article['link']='http://www.santacruzsentinel.com/localnews/ci_22493961/santa-cruzs-cruzio-hosts-open-house-friday-showcase'
        article['date']='1.31.2013'
        article['source']='Santa Cruz Sentinel'
        c.articles.append(article)
        article={}
        article['title']="Officials to Discuss Energy-Saving Options"
        article['link']='http://www.santacruz.com/news/2012/12/04/officials_to_discuss_energy_saving_options'
        article['date']='12.04.2012'
        article['source']='Santa Cruz Weekly'
        c.articles.append(article)
        article={}
        article['title']="Civinomics tech startup to test software at candidate forum"
        article['link']='http://www.santacruzsentinel.com/localnews/ci_21491926/civinomics-tech-startup-test-software-at-candidate-forum'
        article['date']='9.07.2012'
        article['source']='Santa Cruz Sentinel'
        c.articles.append(article)
        article={}
        article['title']="Santa Cruz's Crush on Tech"
        article['link']='http://www.santacruz.com/news/2012/03/20/santa_cruzs_crush_on_tech'
        article['date']='3.20.2012'
        article['source']='Santa Cruz Weekly'
        c.articles.append(article)

        return render('/derived/corp_news.bootstrap')

    def terms(self):
        c.title = 'Terms'
        c.pagetype="terms" 
        return render('/derived/corp_terms.bootstrap')

    def privacy(self):
        c.title = 'Privacy'
        c.pagetype="privacy" 
        return render('/derived/corp_privacy.bootstrap')

    def outreach(self):
        c.title = 'Outreach'
        c.pagetype="outreach" 
        return render('/derived/corp_outreach.bootstrap')

    def contact(self):
        c.title = 'Contact'
        c.pagetype="contact" 
        return render('/derived/corp_contact.bootstrap')



