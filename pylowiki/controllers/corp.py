import logging

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
        c.studies=[]
        scwd2={}
        scwd2["title"]="Santa Cruz and Soquel Creek Water Planning"
        scwd2["description"]="Raising awareness about the regions' water shortage and a proposed desalination plant"
        scwd2["image"]="scwd2_splash_1.26.001.png"
        scwd2["url"]="scwd2"
        c.studies.append(scwd2)
        landtrust={}
        landtrust["title"]="Campaign for 10,000 Acres"
        landtrust["description"]="Collecting ideas on how to save Santa Cruz County's highest priority conservation land"
        landtrust["image"]="Landtrust_2.001.png"
        landtrust["url"]="landtrust"
        c.studies.append(landtrust)
        cap2={}
        cap2["title"]="Santa Cruz Climate Action Plan"
        cap2["description"]="Implenting the City's plan to reduce carbon emissions 30% by 2020"
        cap2["image"]="CAP2.001.jpg"
        cap2["url"]="cap2"
        c.studies.append(cap2)
        eastsideProject={}
        eastsideProject["title"]="Eastside Recycled Water Project"
        eastsideProject["description"]="Siting a new facility to produce recycled water for San Francisco's Downtown"
        eastsideProject["image"]="eastsideProject.001.jpg"
        eastsideProject["url"]="eastsideProject"
        c.studies.append(eastsideProject)
        SSIP={}
        SSIP["title"]="Sewer System Improvement Program"
        SSIP["description"]="Planning for a multi-billion dollar upgrade to San Francisco's sewer system"
        SSIP["image"]="SSIP.001.jpg"
        SSIP["url"]="SSIP"
        c.studies.append(SSIP)

        c.pagetype="casestudies"  
        c.title="Case Studies"
        return render("/derived/corp_listStudies.bootstrap")

    def displayCaseStudy(self, id):
        casestudyname=id
        study={}
        if casestudyname=="scwd2":
            study["url"]="scwd2"
            study["title"]="Santa Cruz and Soquel Creek Water Planning"
            study["image"]="scwd2_splash_1.26.001.png"
            study["statusType"]="important"
            study["statusMessage"]="Closed"
            study["ipadRespondents"]="1,538"
            study["dates"]="9-13-2011 to 3-25-2012"
            study["background"]="The City of Santa Cruz and the Soquel Creek Water District each face a long-term water shortage. Over-pumped groundwater reserves and a federal mandate to reduce intake from streams and rivers to protect fish habitat require the two agencies to improve conservation and develop new supply sources."
            study["solution"]="Civinomics interviewed more than 1,500 residents using iPads to determine base-level awareness of the shortage and get feedback on potential solutions, including conservation and desalination."
            study["results"]="Respondents were enthusiastic about conservation, and 20% signed up for a free home water efficiency audit. Seventy-five percent said that they supported continued study of desalination, but indicated that they would need more information to be sure. Slightly less than 20% (283) of all respondents signed up for continued agency updates on the issue."
            study["nextSteps"]="Civinomics will host an online workshop enabling the community to suggest and refine potential solutions to the region's water shortage. Additional public outreach will take place after the Environmental Impact Report for a regional desalination plant is completed, at which point comprehensive discussion of all options will be possible."
        
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
            study["image"]="Landtrust_2.001.png"
            study["statusType"]="important"
            study["statusMessage"]="Closed"
            study["ipadRespondents"]="500"
            study["dates"]="4-21-2012 to 6-20-2012"
            study["background"]="The Land Trust of Santa Cruz County completed its Conservation Blueprint at the beginning of 2012. This document outlines the most important land in the county to protect based on biodiversity, irreplaceable water resources, and greatest risk for development. The Land Trust currently has the opportunity to acquire the first two major parcels outlined in the Blueprint, CEMEX Redwoods and Star Creek Ranch, and it needs to raise public awareness to get local residents involved in securing these acquisitions."
            study["solution"]="In a pilot outreach campaign, Civinomics interviewed 500 residents using iPads to raise awareness about the Conservation Blueprint and get public input on the managing documents for the new parcels. The outreach did not include fundraising and was purely educational in nature."
            study["results"]="Almost all (98%) of respondents indicated that protecting open space in Santa Cruz County is important to them, with 67% indicating that it is very important. As proof of this, 47% of all respondents opted in with a home address or email address to continue to follow the Land Trust."
            study["nextSteps"]="Civinomics will host an online workshop enabling the community to suggest edits to the new parcels' Conservation Easements - the managing documents for these pieces of conservation land."
            study["videoURL"]="http://player.vimeo.com/video/42731448"

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
            study["image"]="CAP2.001.jpg"
            study["statusType"]="important"
            study["statusMessage"]="Closed"
            study["ipadRespondents"]="500"
            study["dates"]="4-21-12 to 9-1-12"
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
            study["image"]="eastsideProject.001.jpg"
            study["statusType"]="success"
            study["statusMessage"]="Open"
            study["ipadRespondents"]="934"
            study["dates"]="started 2-24-2012"
            study["background"]="The San Francisco Public Utilities Commission (SFPUC) has a goal to provide 4 million gallons per day of recycled water to the City of San Francisco. In order to reach this goal it is building three new recycled water facilities, including one serving Golden Gate Park and one serving the City's downtown, or 'Eastside.' Before selecting a location for the Eastside facility, the SFPUC wants to collect substantial public input. However, it has proven extremely difficult to get the public to show up to in-person forums and workshops."
            study["solution"]="Civinomics created an iPad survey for use in street outreach that discusses the basic principles behind recycled water and its use in San Francisco. The survey then presents each of the potential facility sites, asking respondents to indicate which they prefer, which they oppose and what comments they wish to make. Respondents also supply feedback on whether they prefer a minimal facility or one that includes community space or recreational amenities."
            study["results"]="With Civinomics' help, the SFPUC has been able to collect substantially more public input than ever before. The iPad survey is particularly effective for reaching residents in affected neighborhoods where household access to personal computers or the internet is not a given. Results will be published upon completion of the outreach."
            study["nextSteps"]=""

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
            study["image"]="SSIP.001.jpg"
            study["statusType"]="success"
            study["statusMessage"]="Open"
            study["ipadRespondents"]="1158"
            study["dates"]="started 7-20-2012"
            study["background"]="The San Francisco Public Utilities Commission (SFPUC) is undertaking the multi-billion-dollar Sewer System Improvement Program (SSIP) to modernize the City's infrastructure and ensure the system functions in the event of a major earthquake. These improvements require construction in every neighborhood of the City as well as significant rate increases for residents. A substantial amount of public input is required before and during the project, however, it has proven historically difficult to get the public to show up for in-person forums and workshops."
            study["solution"]="Civinomics created an iPad survey for use in street outreach that provides residents an overview of the SSIP and gauges their support for its different elements. Respondents report sewer related problems, indicate their priorities for the overall project (minimizing costs, reducing odors, creating jobs, etc.) and indicate what they believe to be a reasonable rate increase to cover the cost of the improvements. The surveys are being conducted in the eight watersheds throughout the city."
            study["results"]="Results will be published upon completion of the outreach."
            study["nextSteps"]=""

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


        c.study=study   
        c.pagetype="casestudies"  
        c.title="Case Studies"
        return render("/derived/corp_casestudy.bootstrap")


    def displayCareer(self, id):
        careername=id
        career={}
        if careername=="engfrontend":
            career["title"]="Software Engineer - Front End"
            career["commitment location"]="Fulltime - Santa Cruz, CA"
            career["description"]="We're looking for a capable, quick learner to join our elite enginnering squad and build products for our members and clients. Our culture emphasizes creative problem solving, fast iteration and execution. Join us in our mission to empower communities."

            requirements=[]
            requirement = "CSS"
            requirements.append(requirement)
            requirement = "Javascript and jQuery"
            requirements.append(requirement)
            requirement = "HTML"
            requirements.append(requirement)
            requirement = "Able to work with a small team and quickly adapt"
            requirements.append(requirement)
            requirement = "An eye for UI design"
            requirements.append(requirement)
            career["requirements"]=requirements

            recommendeds=[]
            career["recommendeds"]=recommendeds

        if careername=="engbackend":
            career["title"]="Software Engineer - Back End"
            career["commitment location"]="Fulltime - Santa Cruz, CA"
            career["description"]="We're looking for a capable, quick learner to join our elite enginnering squad and build products for our members and clients. Our culture emphasizes creative problem solving, fast iteration and execution. Join us in our mission to empower communities."

            requirements=[]
            requirement = "Comfortable in a *nix environment"
            requirements.append(requirement)
            requirement = "Python 2.X"
            requirements.append(requirement)
            requirement = "MySQL"
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
            recommended = "Experience with the Pylons framework"
            recommendeds.append(recommended)
            career["recommendeds"]=recommendeds


        if careername=="prep":
            career["title"]="Public Outreach Representative"
            career["commitment location"]="Part time - Santa Cruz and San Francisco, CA"
            career["description"]="Person-to-person interaction is still the most effective means of community engagement, that's why we decided to re-invent the practice for the 21st century. We conduct face-to-face interviews for public agencies and non-profits via iPad. We are looking to hire new field organizers for the purposes of conducting surveys both at community events and through door-to-door outreach. We do not fundraise - our campaigns are educational and research oriented. Previous experience is recommended, but not required. Community Representatives are paid $3.00 per interview, most complete between 5-8 interviews per hour. We are looking to fill these positions ASAP."

            requirements=[]
            requirement = "Effective Communication"
            requirements.append(requirement)
            requirement = "Cultural Competency"
            requirements.append(requirement)
            requirement = "The ability to be polite and respectful"
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
        return render('/derived/corp_team.bootstrap')

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



