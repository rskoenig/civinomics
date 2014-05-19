<%!    
    import logging
    log = logging.getLogger(__name__)
%>

################################################
## D3 graphs
################################################

<%def name="includeD3()">
  <script src="/js/vendor/d3.v3.min.js" charset="utf-8"></script>
  <link href='/styles/d3Custom.css' rel='stylesheet' type='text/css'>
</%def>

<%def name="dcPlasticBagSurvey()">

    <script src='/js/vendor/crossfilter111.min.js' type='text/javascript'></script>
    <script src='/js/vendor/dc130.min.js' type='text/javascript'></script>
    <script src='/js/vendor/underscore-min.js' type='text/javascript'></script>
    <link href='/styles/vendor/dc.css' rel='stylesheet' type='text/css'>

    <hr>
    <div class='row' name="dc-data-top" data-spy="affix" data-offset-top="1150" >
        <div class="col-sm-12">
            <div class="pull-left workshop-metrics metrics-large">
                Results
            </div>
            <div class="dc-data-count well" data-spy="affix" data-offset-top="650" style="float: right; margin-top: 0;"> 
                <span> 
                    <span class="filter-count"></span>
                    selected out of
                    <span class="total-count"></span> 
                    records | <a href="#dc-data-top" name="dc-data-count" onclick="javascript:dc.filterAll(); dc.renderAll();">Reset</a>
                </span>
            </div>
        </div>
    </div>
    <div class='row'>   
        <div class='col-sm-6'>
            <p class="lead">The majority of Scotts Valley residents are aware of the other plastic bag bans in Santa Cruz County.</p>
            <h4>Question: "Have you heard about the plastic bag bans in Santa Cruz County?"</h4>
        </div>
        <div class='col-sm-6' id='dc-heardOfBagBans-chart'> 
                <span>
                    <a href="#dc-data-top" class="reset"
    onclick="javascript:heardOfBagBansChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
        </div>
    </div><!-- row --> 
    <hr>
    <div class="row">
        <div class="col-sm-6">
            <p class="lead">About half of respondents (48%) believe the existing bag bans have had a positive effect. 15% believe they've had no effect or a negative effect.</p>
            <h4>Question: "What is your impression of the Santa Cruz plastic bag bans?"</h4>
        </div>
        <div class='col-sm-6' id='dc-impressionOfBagBans-chart'>
            <span>
                <a href="#dc-data-top" class="reset"
onclick="javascript:impressionOfBagBansChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
            </span>
        </div>
    </div>
    <hr>
    <div class="row">
        <div class="col-sm-6">
            <p class="lead">32% of respondents were aware that a bag ban had been proposed for the City of Scotts Valley</p>
            <h4>Question: "Have you heard about the proposed Plastic Bag Ban for Scotts Valley?"</h4>
        </div>
        <div class='col-sm-6' id='dc-proposedBagBan-chart'>
            <span>
                <a href="#dc-data-top" class="reset"
onclick="javascript:proposedBagBanChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
            </span>
        </div>
    </div>
    <hr>
    <div class='row'>   
        <div class='col-sm-6'> 
            <p class="lead">72% of Scotts Valley residents would vote "YES" for a City of Scotts Valley plastic bag ban.</p>
            <h4>Question: "If the vote were held today on the Plastic Bag Ban, would you vote 'YES' in favor of it or 'NO' to oppose it?"</h4>
        </div>
        <div class="col-sm-6" id='dc-voteInFavor-chart'>
            <span>
                    
                    <a href="#dc-data-top" class="reset"
    onclick="javascript:voteInFavorChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
        </div>
    </div>
    <hr>
    <div class="row">
        <div class='col-sm-6'>
            <p class="lead">64% of residents would still support a Plastic Bag Ban if it had a $0.10 fee.</p>
            <h4>Question: "How about if the Plastic Bag Ban included a fee of $0.10 on paper bags? Would you vote "yes" or "no" on this measure?"</h4>
        </div>
        <div class='col-sm-6' id='dc-includeFeeVoteYes-chart'>
                <span>
                    
                    <a href="#dc-data-top" class="reset"
    onclick="javascript:includeFeeVoteYesChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
        </div>
    </div>
    <hr>
    <h4>
        "Next, you will read a few of the reasons that some people and organizations may give for being in favor of the measure to implement a Plastic Bag Ban and an accompanying Fee for Paper Bags. Please indicate if each one makes you much more likely to favor the measure, somewhat more likely to favor it, or if the statement makes no difference to you one way or the other."
    </h4>
    <hr>
    <div class='row'>   
        <div class="col-sm-6">
            <p class="lead">82% of respondents who indicated that they would vote "Probably No" on a Bag Ban, indicated that they were "somewhat" to "much more likely to supprot a ban" with this information.</p>
            <h4>Question: "Save Our Shores reports that the number of plastic bags collected during beach cleanups has decreased 80% since the passage of the Santa Cruz bans. Does this make you..."</h4>
        </div>
        <div class='col-sm-6' id='dc-bagsFoundDecreased-chart'>
                <span>
                    
                    <a href="#dc-data-top" class="reset"
    onclick="javascript:bagsFoundDecreasedChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
        </div>
    </div>
    <hr>
    <div class="row">
        <div class="col-sm-6">
            <p class="lead">88% of respondents who indicated that they would vote "Probably No" on a Bag Ban, indicated that they were "somewhat" to "much more likely to supprot a ban" with this information.</p>
            <h4>Question: "The Monterey Bay Aquarium Research Institute has observed thousands of pieces of trash in our marine sanctuary's deep sea trench with plastic bags being the most common type of trash. Does this make you..."</h4>
        </div>
        <div class='col-sm-6' id='dc-trenchHasBags-chart'> 
                <span>
                    
                    <a href="#dc-data-top" class="reset"
    onclick="javascript:trenchHasBagsChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
        </div>
    </div>
    <hr>
    <div class="row">
        <div class="col-sm-6">
            <p class="lead">49% of respondents who indicated that they would vote "Probably No" on a Bag Ban with a $0.10 fee, indicated that they were "somewhat" to "much more likely to supprot a ban" with this information.</p>
            <h4>Question: "The only region that didn't include a fee along with their plastic bag ban (Carmel) saw NO increase in reusable bag usage. (Compared to a 28% increase in regions that did include a fee). Does this make you.."</h4>

        </div>
        <div class='col-sm-6' id='dc-carmelDoesntFee-chart'>
            <span>
                
                <a href="#dc-data-top" class="reset"
onclick="javascript:carmelDoesntFeeChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
            </span>
        </div>
    </div>
    <hr>
    <div class="row">
        <div class="col-sm-6">
            <p class="lead">49% of respondents who indicated that they would vote "Probably No" on a Bag Ban with a $0.10 fee, indicated that they were "somewhat" to "much more likely to supprot a ban" with this information.</p>
            <h4>Question: "The high environmental and energy costs of producing paper bags is well documented by the scientific community. For this reason, proponents of reusable bags say we cannot simply substitute paper for plastic. Does this make you..."</h4>
        </div class="col-sm-6">
        <div class='col-sm-6' id='dc-highCostsPlasticBags-chart'>
                <span>
                    
                    <a href="#dc-data-top" class="reset"
    onclick="javascript:highCostsPlasticBagsChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
        </div>
    </div>
    <hr>
    <div class="row">
        <div class="col-sm-6">
            <p class="lead">34% of respondents who indicated that they would vote "Probably No" on a Bag Ban with a $0.10 fee, indicated that they were "somewhat" to "much more likely to supprot a ban" with this information.</p>
            <h4>Question: "Every other City in the County of Santa Cruz has implemented a plastic bag ban and accompanying fee. Does this make you..."</h4>
        </div>
        <div class='col-sm-6' id='dc-everyOtherCityFees-chart'> 
                <span>
                    
                    <a href="#dc-data-top" class="reset"
    onclick="javascript:everyOtherCityFeesChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
        </div>
    </div>
    <hr>
    <div class="workshop-metrics metrics-large">
        Demographics / Population Segments
    </div>
    <hr>
    <div class="row">
        <div class='col-sm-4' id='dc-localMerchant-chart'>
            <h4>Are you a local merchant?
                <span>
                    
                    <a href="#dc-data-top" class="reset"
    onclick="javascript:localMerchantChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4> 
        </div>
        <div class='col-sm-4' id='dc-ageLower-chart'> 
            <h4>Age
                <span>
                    <br />(drag sliders to filter results)
                </span>
            </h4>
        </div>
        <div class='col-sm-4' id='dc-gender-chart'>
            <h4>Gender
                <span>
                    
                    <a href="#dc-data-top" class="reset"
    onclick="javascript:genderChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4> 
        </div>
    </div><!-- row -->
    <!-- ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^  -->
    <hr>
    <div class='row'>   
        <div class='col-sm-4' id='dc-childrenInHome-chart'>
            <h4>Are there any children, 17 years of age or younger, living in your household?
                <span>
                    
                    <a href="#dc-data-top" class="reset"
    onclick="javascript:childrenInHomeChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a>
                </span>
            </h4> 
        </div>
        <div class='col-sm-4' id='dc-howLongInSC-chart'>
            <h4>For about how long have you lived in Santa Cruz County?
                <span>
                    
                    <a href="#dc-data-top" class="reset"
    onclick="javascript:howLongInSCChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4> 
        </div>
    </div>
    <!-- ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^  -->
    <hr>
    <div class="workshop-metrics metrics-large">
        Comments and Suggestions
    </div>
    <hr>
    <div class='row'> 
        <div class='col-xs-12' id='dc-commentsOrSuggestions-chart'>
          <div id="commentsOrSuggestionsContainer">
          </div>
        </div>
    </div>

    <script>
        // Create the dc.js chart objects & link to div
        var heardOfBagBansChart = dc.pieChart("#dc-heardOfBagBans-chart");
        var impressionOfBagBansChart = dc.rowChart("#dc-impressionOfBagBans-chart");
        var proposedBagBanChart = dc.pieChart("#dc-proposedBagBan-chart");
        var voteInFavorChart = dc.rowChart("#dc-voteInFavor-chart");
        var includeFeeVoteYesChart = dc.rowChart("#dc-includeFeeVoteYes-chart");
        var bagsFoundDecreasedChart = dc.rowChart("#dc-bagsFoundDecreased-chart");
        var trenchHasBagsChart = dc.rowChart("#dc-trenchHasBags-chart");
        var carmelDoesntFeeChart = dc.rowChart("#dc-carmelDoesntFee-chart");
        var highCostsPlasticBagsChart = dc.rowChart("#dc-highCostsPlasticBags-chart");
        var everyOtherCityFeesChart = dc.rowChart("#dc-everyOtherCityFees-chart");
        var howLongInSCChart = dc.rowChart("#dc-howLongInSC-chart");
        var localMerchantChart = dc.pieChart("#dc-localMerchant-chart");
        var ageLowerChart = dc.barChart("#dc-ageLower-chart");
        var genderChart = dc.pieChart("#dc-gender-chart");
        var childrenInHomeChart = dc.pieChart("#dc-childrenInHome-chart");


        d3.csv("/surveys/plastic_bag3.csv", function(error, data) {
            //console.log(error);
            //console.log(data);
            var impressionOfBagBansValues = {};
            var voteInFavorValues = {};
            var includeFeeVoteYesValues = {};
            var bagsFoundDecreasedValues = {};
            var trenchHasBagsValues = {};
            var carmelDoesntFeeValues = {};
            var highCostsPlasticBagsValues = {};
            var everyOtherCityFeesValues = {};
            var howLongInSCValues = {};
            i = 0;
            data.forEach(function(d) {
                i++;
                d.ageLower = +d.ageLower;
                if (d.impressionOfBagBans == "") {
                    impressionOfBagBansValues[d.impressionOfBagBans] = i + '^' + 'No answer';
                } else {
                    impressionOfBagBansValues[d.impressionOfBagBans] = i + '^' + d.impressionOfBagBans;
                }
                if (d.voteInFavor == "") {
                    voteInFavorValues[d.voteInFavor] = i + '^' + 'No answer';
                } else {
                    voteInFavorValues[d.voteInFavor] = i + '^' + d.voteInFavor;    
                }
                if (d.includeFeeVoteYes == "") {
                    includeFeeVoteYesValues[d.includeFeeVoteYes] = i + '^' + 'No answer';
                } else {
                    includeFeeVoteYesValues[d.includeFeeVoteYes] = i + '^' + d.includeFeeVoteYes;
                }
                if (bagsFoundDecreasedValues == "") {
                    bagsFoundDecreasedValues[d.bagsFoundDecreased] = i + '^' + 'No answer';
                } else {
                    bagsFoundDecreasedValues[d.bagsFoundDecreased] = i + '^' + d.bagsFoundDecreased;   
                }
                if (d.trenchHasBags == "") {
                    trenchHasBagsValues[d.trenchHasBags] = i + '^' + 'No answer';
                } else {
                    trenchHasBagsValues[d.trenchHasBags] = i + '^' + d.trenchHasBags;
                }
                if (d.carmelDoesntFee == "") {
                    carmelDoesntFeeValues[d.carmelDoesntFee] = i + '^' + 'No answer';
                } else {
                    carmelDoesntFeeValues[d.carmelDoesntFee] = i + '^' + d.carmelDoesntFee;
                }

                if (d.highCostsPlasticBags == "") {
                    highCostsPlasticBagsValues[d.highCostsPlasticBags] = i + '^' + 'No answer';
                } else {
                    highCostsPlasticBagsValues[d.highCostsPlasticBags] = i + '^' + d.highCostsPlasticBags;
                }

                if (d.everyOtherCityFees == "") {
                    everyOtherCityFeesValues[d.everyOtherCityFees] = i + '^' + 'No answer';
                } else {
                    everyOtherCityFeesValues[d.everyOtherCityFees] = i + '^' + d.everyOtherCityFees;
                }

                if (d.howLongInSC == "") {
                    howLongInSCValues[d.howLongInSC] = i + '^' + 'No answer';
                } else {
                    howLongInSCValues[d.howLongInSC] = i + '^' + d.howLongInSC;
                }

                if (d.commentsOrSuggestions != "") {
                    $('#commentsOrSuggestionsContainer').append('<p>* ' + d.commentsOrSuggestions + '</p>');
                }                
            });

            // Run the data through crossfilter and load our 'facts'
            var facts = crossfilter(data);

            // reset all button - this includes all facts
            var all = facts.groupAll();

            // reset all button - count all the facts
            dc.dataCount(".dc-data-count") 
                .dimension(facts) 
                .group(all);
            dc.dataCount(".dc-data-count2") 
                .dimension(facts) 
                .group(all);


            /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
            var heardOfBagBans = facts.dimension(function (d) { 
                if (d.heardOfBagBans == "") {
                    return "No answer";
                } else {
                    return d.heardOfBagBans;
                }
            });
            var heardOfBagBansGroup = heardOfBagBans.group();
 
            var impressionOfBagBans = facts.dimension(function (d) {
                // for row charts, we return a predefined string: "#.string"
                return impressionOfBagBansValues[d.impressionOfBagBans]
            });
            var impressionOfBagBansGroup = impressionOfBagBans.group();

            var proposedBagBan = facts.dimension(function (d) {
                if (d.proposedBagBan == "") {
                    return "No answer";
                } else {
                    return d.proposedBagBan;
                }
            });
            var proposedBagBanGroup = proposedBagBan.group();

            var voteInFavor = facts.dimension(function (d) {
                return voteInFavorValues[d.voteInFavor]
            });
            var voteInFavorGroup = voteInFavor.group();

            var includeFeeVoteYes = facts.dimension(function (d) {
                return includeFeeVoteYesValues[d.includeFeeVoteYes];
            });
            var includeFeeVoteYesGroup = includeFeeVoteYes.group();

            var bagsFoundDecreased = facts.dimension(function (d) {
                return bagsFoundDecreasedValues[d.bagsFoundDecreased];
                
            });
            var bagsFoundDecreasedGroup = bagsFoundDecreased.group();

            var trenchHasBags = facts.dimension(function (d) {
                return trenchHasBagsValues[d.trenchHasBags];
            });
            var trenchHasBagsGroup = trenchHasBags.group();

            var carmelDoesntFee = facts.dimension(function (d) {
                return carmelDoesntFeeValues[d.carmelDoesntFee];
            });
            var carmelDoesntFeeGroup = carmelDoesntFee.group();

            var highCostsPlasticBags = facts.dimension(function (d) {
                return highCostsPlasticBagsValues[d.highCostsPlasticBags];
            });
            var highCostsPlasticBagsGroup = highCostsPlasticBags.group();

            var everyOtherCityFees = facts.dimension(function (d) {
                return everyOtherCityFeesValues[d.everyOtherCityFees];
            });
            var everyOtherCityFeesGroup = everyOtherCityFees.group();

            var howLongInSC = facts.dimension(function (d) {
                return howLongInSCValues[d.howLongInSC];
            });
            var howLongInSCGroup = howLongInSC.group();

            var localMerchant = facts.dimension(function (d) {
                if (d.localMerchant == "") {
                    return "No answer";
                } else {
                    return d.localMerchant;
                }
            });
            var localMerchantGroup = localMerchant.group();

            var ageLower = facts.dimension(function (d) {
                return d.ageLower;
            });
            var ageLowerGroup = ageLower.group();

            var gender = facts.dimension(function (d) {
                if (d.gender == "") {
                    return "No answer";
                } else {
                    return d.gender;
                }
            });
            var genderGroup = gender.group();

            var childrenInHome = facts.dimension(function (d) {
                if (d.childrenInHome == "") {
                    return "No answer";
                } else {
                    return d.childrenInHome;
                }
            });
            var childrenInHomeGroup = childrenInHome.group();

            var peopleFormatter = function(d) {
                if (d > 1)
                    return d + " people";
                else if (d == 1)
                    return d + " person";
                else
                    return d;
            }

            var piePercentage = function(d, sumgroup) {
                //var percent = d.data.key;
                var fraction = d.value / _.reduce(sumgroup.all(), function(memo, d){ return memo + d.value; }, 0);
                var percent = Math.round(fraction * 100);
                var phrase = "";
                if (d.data) {
                    phrase = d.data.key + "  " + percent + "%";    
                } else {
                    phrase = percent + "%";    
                }
                return phrase;
            }
            var yearsFormatter = function(d) {
                var yearText = (d == 0 ? d : d + " years");
                return yearText;
            }
            heardOfBagBansChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(heardOfBagBans) 
                .group(heardOfBagBansGroup)
                .label(function(d){return piePercentage(d, heardOfBagBansGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});  
            
            impressionOfBagBansChart.width(300) 
                .height(220)
                .margins({top: 5, right: 1, bottom: 20, left: 6})
                .dimension(impressionOfBagBans) 
                .group(impressionOfBagBansGroup)
                .colors(d3.scale.category20b())
                .label(function (d){
                  return d.key.split('^')[1];
                  })
                .title(function(d){return d.key.split('^')[1] + ", " + piePercentage(d, impressionOfBagBansGroup);})
                .xAxis()
                .tickFormat(function(d) { return d; })
                .ticks(4);

            proposedBagBanChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(proposedBagBan) 
                .group(proposedBagBanGroup) 
                .label(function(d){return piePercentage(d, proposedBagBanGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});

            voteInFavorChart.width(300) 
                .height(220) 
                .margins({top: 5, right: 1, bottom: 20, left: 6})
                .dimension(voteInFavor) 
                .group(voteInFavorGroup)
                .colors(d3.scale.category20())
                .label(function (d){
                  return d.key.split('^')[1];
                  }) 
                .title(function(d){return d.key.split('^')[1] + ", " + piePercentage(d, voteInFavorGroup);})
                .xAxis()
                .tickFormat(function(d) { return d; })
                .ticks(4);

            includeFeeVoteYesChart.width(300)
                .height(220) 
                .margins({top: 5, right: 1, bottom: 20, left: 6})
                .dimension(includeFeeVoteYes) 
                .group(includeFeeVoteYesGroup)
                .colors(d3.scale.category20())
                .label(function (d){
                  return d.key.split('^')[1];
                  }) 
                .title(function(d){return d.key.split('^')[1] + ", " + piePercentage(d, includeFeeVoteYesGroup);})
                .xAxis()
                .tickFormat(function(d) { return d; })
                .ticks(4);

            bagsFoundDecreasedChart.width(300)
                .height(220) 
                .margins({top: 5, right: 1, bottom: 20, left: 6})
                .dimension(bagsFoundDecreased) 
                .group(bagsFoundDecreasedGroup)
                .colors(d3.scale.category20c())
                .label(function (d){
                  return d.key.split('^')[1];
                  }) 
                .title(function(d){return d.key.split('^')[1] + ", " + piePercentage(d, includeFeeVoteYesGroup);})
                .xAxis()
                .tickFormat(function(d) { return d; })
                .ticks(4);

            trenchHasBagsChart.width(300)
                .height(220) 
                .margins({top: 5, right: 1, bottom: 20, left: 6})
                .dimension(trenchHasBags) 
                .group(trenchHasBagsGroup)
                .colors(d3.scale.category20b())
                .label(function (d){
                  return d.key.split('^')[1];
                  }) 
                .title(function(d){return d.key.split('^')[1] + ", " + piePercentage(d, trenchHasBagsGroup);})
                .xAxis()
                .tickFormat(function(d) { return d; })
                .ticks(4);

            carmelDoesntFeeChart.width(300)
                .height(220) 
                .margins({top: 5, right: 1, bottom: 20, left: 6})
                .dimension(carmelDoesntFee) 
                .group(carmelDoesntFeeGroup)
                .colors(d3.scale.category10())
                .label(function (d){
                  return d.key.split('^')[1];
                  }) 
                .title(function(d){return d.key.split('^')[1] + ", " + piePercentage(d, carmelDoesntFeeGroup);})
                .xAxis()
                .tickFormat(function(d) { return d; })
                .ticks(4);

            highCostsPlasticBagsChart.width(300)
                .height(220) 
                .margins({top: 5, right: 1, bottom: 20, left: 6})
                .dimension(highCostsPlasticBags) 
                .group(highCostsPlasticBagsGroup)
                .colors(d3.scale.category20())
                .label(function (d){
                  return d.key.split('^')[1];
                  }) 
                .title(function(d){return d.key.split('^')[1] + ", " + piePercentage(d, highCostsPlasticBagsGroup);})
                .xAxis()
                .tickFormat(function(d) { return d; })
                .ticks(4);

            everyOtherCityFeesChart.width(300)
                .height(220) 
                .margins({top: 5, right: 1, bottom: 20, left: 6})
                .dimension(everyOtherCityFees) 
                .group(everyOtherCityFeesGroup)
                .colors(d3.scale.category20b())
                .label(function (d){
                  return d.key.split('^')[1];
                  }) 
                .title(function(d){return d.key.split('^')[1] + ", " + piePercentage(d, everyOtherCityFeesGroup);})
                .xAxis()
                .tickFormat(function(d) { return d; })
                .ticks(4);
                
            howLongInSCChart.width(270)
                .height(220) 
                .margins({top: 5, right: 1, bottom: 20, left: 6})
                .dimension(howLongInSC) 
                .group(howLongInSCGroup)
                .colors(d3.scale.category20c())
                .label(function (d){
                  return d.key.split('^')[1];
                  }) 
                .title(function(d){return d.key.split('^')[1] + ", " + piePercentage(d, howLongInSCGroup);})
                .xAxis()
                .tickFormat(function(d) { return d; })
                .ticks(4);

            localMerchantChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(localMerchant) 
                .group(localMerchantGroup)
                .label(function(d){return piePercentage(d, localMerchantGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});  
            
            ageLowerChart.width(264) 
                .height(220) 
                .margins({top: 5, right: 1, bottom: 20, left: 30})
                .dimension(ageLower) 
                .group(ageLowerGroup) 
                .transitionDuration(500) 
                .centerBar(true) 
                .gap(-8)
                .filter([0, 79]) 
                .x(d3.scale.linear().domain([0, 80])) 
                .elasticY(true)
                .xAxis()
                .tickFormat(function(d) { return yearsFormatter(d); })
                .ticks(6);

            genderChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(gender) 
                .group(genderGroup)
                .label(function(d){return piePercentage(d, genderGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});  

            childrenInHomeChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(childrenInHome) 
                .group(childrenInHomeGroup)
                .label(function(d){return piePercentage(d, childrenInHomeGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});  

            // Render the Charts
            dc.renderAll();

        });

    </script>

</%def>


<%def name="dcDmcSurvey()">
  
    <script src='/js/vendor/crossfilter111.min.js' type='text/javascript'></script>
    <script src='/js/vendor/dc130.min.js' type='text/javascript'></script>
    <script src='/js/vendor/underscore-min.js' type='text/javascript'></script>
    <link href='/styles/vendor/dc.css' rel='stylesheet' type='text/css'>

    <div class='row' name="dc-data-top">
        <div class="pull-left workshop-metrics metrics-large">
            Results
        </div>
        <div class="dc-data-count well" data-spy="affix" data-offset-top="650" style="float: right; margin-top: 0;"> 
            <span> 
                <span class="filter-count"></span>
                selected out of
                <span class="total-count"></span> 
                records | <a href="#dc-data-top" name="dc-data-count" onclick="javascript:dc.filterAll(); dc.renderAll();">Reset</a>
            </span>
        </div>
    </div>

    <!-- ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^  -->
    <div class='row'>   
        <div class='span4' id='dc-familiarDtProgram-chart'>
            <h4>How familiar are you with the Downtown Hospitality Program?
                <span>
                    
                    <a href="#dc-data-top" class="reset"
    onclick="javascript:familiarDtProgramChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4> 
        </div>
        <div class="span8">
            <p class="lead"><em>"The Downtown Hospitality Program was created and paid for by downtown business and property owners to maintain a safe and friendly environment. "Hosts" can be contacted as an alternative to police to help with aggressive panhandling and other forms of anti-social behavior. They also serve as an additional resource for visitors and downtown shoppers, and provide a visible presence in downtown to observe, report and prevent street disorder. The program is overseen by the Downtown Management Corporation (DMC), which also contributes funding for the downtown trolley."</em></p> 
        </div>
    </div>
    <!-- ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^  -->
    <hr>
    <div class="row">
        <div class='span4' id='dc-feelSafeWorkingDt-chart'>
            <h4>In general, do you feel safe working downtown?
                <span>
                    
                    <a href="#dc-data-top" class="reset"
onclick="javascript:feelSafeWorkingDtChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4> 
        </div>
        <div class='span4' id='dc-believeDtProgramMakesSafer-chart'>
            <h4>In general, do you believe the Downtown Hospitality Program makes downtown safer?
                <span>
                    
                    <a href="#dc-data-top" class="reset"
onclick="javascript:believeDtProgramMakesSaferChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4> 
        </div>
        <div class='span4' id='dc-howEffectiveResolveBehavior-chart'>
            <h4>In your opinion, how effective is the program at addressing and resolving anti-social behavior?
                <span>
                    
                    <a href="#dc-data-top" class="reset"
onclick="javascript:howEffectiveResolveBehaviorChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4> 
        </div>
    </div>
    <!-- ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^  -->
    <hr>
    <div class='row'>
        <div class='span4' id='dc-everWitnessedProgramHost-chart'>
            <h4>Have you ever contacted, or witnessed a coworker/employee contact a downtown hospitality host?
                <br /><a href="#everWitnessedProgramHostDescription">see descriptions</a>
                <span>
                    
                    <a href="#dc-data-top" class="reset"
onclick="javascript:everWitnessedProgramHostChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4> 
        </div>
        <div class='span4' id='dc-hostApproachable-chart'>
            <h4>In your opinion, how approachable are the downtown hospitality hosts?
                <span>
                    
                    <a href="#dc-data-top" class="reset"
onclick="javascript:hostApproachableChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4> 
        </div>
        <div class='span4' id='dc-howOftenSeeHost-chart'>
            <h4>How often do you see a downtown hospitality host?
                <span>
                    
                    <a href="#dc-data-top" class="reset"
onclick="javascript:howOftenSeeHostChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4>
        </div>
    </div>
    <!-- ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^  -->
    <hr>
    <div class='row'>
        <div class='span4' id='dc-howOftenInteractWithPeople-chart'>
            <h4>When you see a hospitality host, how often are they interacting with visitors and shoppers?
                <br /><a href="#additionalServicesSuggestions">see service suggestions</a>
                <span>
                    
                    <a href="#dc-data-top" class="reset"
onclick="javascript:howOftenInteractWithPeopleChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4>
        </div>
    </div><!-- row -->
    <!-- ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^  -->
    <hr>
    <div class="row">
        <div class='col-sm-6' id='dc-opinionFirstPriorityForServices-chart'>
            <h4>In your opinion, what should be the DMC's first priority in terms of downtown programing and services?
                <br /><a href="#opinionFirstPriorityForServices1">see additional suggestions</a>
                <span>
                    
                    <a href="#dc-data-top" class="reset"
onclick="javascript:opinionFirstPriorityForServicesChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4>
        </div>
        <div class='col-sm-6' id='dc-mostImportantAboutHosts-chart'>
            <h4>Out of the following additional services the DMC could provide, which would be the most important to you?
                <br /><a href="#mostImportantAboutHosts1">see further input</a>
                <span>
                    
                    <a href="#dc-data-top" class="reset"
    onclick="javascript:mostImportantAboutHostsChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4>
        </div>
    </div>
    <hr>
    <div class="workshop-metrics metrics-large">
        Demographics / Business Type
    </div>
    <hr>
    <div class="row">
        <div class='span4' id='dc-whatDescribesYourBusiness-chart'>
            <h4>Which of the following best describes your business or working environment?
                <span>
                    
                    <a href="#dc-data-top" class="reset"
onclick="javascript:whatDescribesYourBusinessChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4>
        </div>
        <div class='span4' name='dc-yourRoleInBusiness-chart' id='dc-yourRoleInBusiness-chart'>
            <h4>What is your role in the business?
                <br /><a href="#yourRoleInBusiness1">see further comments</a>
                <span>
                    
                    <a href="#dc-data-top" class="reset"
onclick="javascript:yourRoleInBusinessChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4>
        </div>
        <div class='span4' id='dc-gender-chart'>
            <h4>Gender
                <span>
                    
                    <a href="#dc-data-top" class="reset"
onclick="javascript:genderChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
                </span>
            </h4>
        </div>
    </div>
    <hr>
    <div class='row'>
        <div class='span4' id='dc-ageLower-chart'> 
            <h4>Age of respondents
                <span>
                    (drag sliders to filter results)
                </span>
            </h4>
        </div>
    </div>
    <hr>
    <div class='row'> 
        <div class='span12'>
            <h4 name='everWitnessedProgramHostDescription'>Can you please briefly describe your experience? Was it positive?
                <a href="#dc-everWitnessedProgramHost-chart"><br />Responses to question: "Have you ever contacted, or witnessed a coworker/employee contact a downtown hospitality host?"</a>
            </h4>
            <div id="everWitnessedProgramHostDescription"></div>
        </div>
    </div>
    <div class='row'> 
        <div class='span12'>
            <h4 name='howOftenInteractWithPeople'>Additional services suggested for:
                <a href="#dc-everWitnessedProgramHost-chart"><br />"When you see a hospitality host, how often are they interacting with visitors and shoppers?"</a>
            </h4>
            <div id="additionalServicesSuggestions"></div>
        </div>
    </div>
    <div class='row'> 
        <div class='span12'>
            <h4 name='mostImportantAboutHosts1'>Further input on question: 
                <a href="#dc-mostImportantAboutHosts-chart"><br />"Out of the following additional services the DMC could provide, which would be the most important to you?"</a>
            </h4>
            <div id="mostImportantAboutHosts1"></div>
            <div id="mostImportantAboutHosts2"></div>
        </div>
    </div>
    <div class='row'> 
        <div class='span12'>
            <h4 name='opinionFirstPriorityForServices1'>Additional suggestions for:
                <a href="#dc-opinionFirstPriorityForServices-chart"><br />"In your opinion, what should be the DMC's first priority in terms of downtown programing and services?"</a>
            </h4>
            <div id="opinionFirstPriorityForServices1"></div>
        </div>
    </div>
    <div class='row'> 
        <div class='span12'>
            <h4 name='improvementsForYourSafety1'>Additional suggestions for:
                <a href="#dc-improvementsForYourSafety-chart"><br />"What improvements, if any, could be made to improve your feeling of safety in the downtown area? (check all that apply)"</a>
            </h4>
            <div id="improvementsForYourSafety1"></div>
        </div>
    </div>
    <div class='row'> 
        <div class='span12'>
            <h4 name='whatDescribesYourBusiness1'>Additional input from:
                <a href="#dc-whatDescribesYourBusiness-chart"><br />"Which of the following best describes your business or working environment?"</a>
            </h4>
            <div id="whatDescribesYourBusiness1"></div>
        </div>
    </div>
    
    

    <script>
        // Create the dc.js chart objects & link to div
        var ageLowerChart = dc.barChart("#dc-ageLower-chart");
        var familiarDtProgramChart = dc.pieChart("#dc-familiarDtProgram-chart");
        var yourRoleInBusinessChart = dc.pieChart("#dc-yourRoleInBusiness-chart");

        var feelSafeWorkingDtChart = dc.pieChart("#dc-feelSafeWorkingDt-chart");
        var believeDtProgramMakesSaferChart = dc.pieChart("#dc-believeDtProgramMakesSafer-chart");
        var howEffectiveResolveBehaviorChart = dc.pieChart("#dc-howEffectiveResolveBehavior-chart");

        var everWitnessedProgramHostChart = dc.pieChart("#dc-everWitnessedProgramHost-chart");
        
        var hostApproachableChart = dc.pieChart("#dc-hostApproachable-chart");

        var howOftenSeeHostChart = dc.pieChart("#dc-howOftenSeeHost-chart");
        var howOftenInteractWithPeopleChart = dc.pieChart("#dc-howOftenInteractWithPeople-chart");
        var mostImportantAboutHostsChart = dc.rowChart("#dc-mostImportantAboutHosts-chart");


        var opinionFirstPriorityForServicesChart = dc.pieChart("#dc-opinionFirstPriorityForServices-chart");
        
        var improvementsForYourSafetyChart = dc.rowChart("#dc-improvementsForYourSafety-chart");

        var whatDescribesYourBusinessChart = dc.rowChart("#dc-whatDescribesYourBusiness-chart");

        var genderChart = dc.pieChart("#dc-gender-chart");

        var data = null;
        
        // NOTE: the csv file's fields tend to get wrapped in apostrophes thanks to open office:
        // ( "field", "field", .. )
        //   remove these or the csv loader here won't work e.g.: ( field, field, .. )
        d3.csv("/surveys/dmc_survey2.csv", function(error, data) {
            //console.log(error);
            //console.log(data);
            var mostImportantAboutHostsValues = {};
            var improvementsForYourSafetyValues = {};
            var whatDescribesYourBusinessValues = {};
            i = 0;
            data.forEach(function(d) {
                i++;
                d.ageUpper = +d.ageUpper;
                d.ageLower = +d.ageLower;
                if (d.yourRoleInBusiness1 != "") {
                    $('#yourRoleInBusiness1').append('<p>* ' + d.yourRoleInBusiness1 + '</p>');
                }       
                if (d.everWitnessedProgramHostDescription != "") {
                    $('#everWitnessedProgramHostDescription').append('<p>* ' + d.everWitnessedProgramHostDescription + '</p>');
                }
                if (d.additionalServicesSuggestions != "") {
                    $('#additionalServicesSuggestions').append('<p>* ' + d.additionalServicesSuggestions + '</p>');
                }
                if (d.opinionFirstPriorityForServices1 != "") {
                    $('#opinionFirstPriorityForServices1').append('<p>* ' + d.opinionFirstPriorityForServices1 + '</p>');
                }
                if (d.mostImportantAboutHosts == "") {
                    mostImportantAboutHostsValues[d.mostImportantAboutHosts] = i + '^' + 'No answer';
                } else {
                    mostImportantAboutHostsValues[d.mostImportantAboutHosts] = i + '^' + d.mostImportantAboutHosts;   
                }
                if (d.mostImportantAboutHosts1 != "") {
                    $('#mostImportantAboutHosts1').append('<p>* ' + d.mostImportantAboutHosts1 + '</p>');
                }
                if (d.mostImportantAboutHosts2 != "") {
                    $('#mostImportantAboutHosts2').append('<p>* ' + d.mostImportantAboutHosts2 + '</p>');
                }
                if (d.improvementsForYourSafety == "") {
                    improvementsForYourSafetyValues[d.improvementsForYourSafety] = i + '^' + 'No answer';
                } else {
                    improvementsForYourSafetyValues[d.improvementsForYourSafety] = i + '^' + d.improvementsForYourSafety;   
                }
                if (d.improvementsForYourSafety1 != "") {
                    $('#improvementsForYourSafety1').append('<p>* ' + d.improvementsForYourSafety1 + '</p>');
                }
                if (d.whatDescribesYourBusiness == "") {
                    whatDescribesYourBusinessValues[d.whatDescribesYourBusiness] = i + '^' + 'No answer';
                } else {
                    whatDescribesYourBusinessValues[d.whatDescribesYourBusiness] = i + '^' + d.whatDescribesYourBusiness;   
                }
                if (d.whatDescribesYourBusiness1 != "") {
                    $('#whatDescribesYourBusiness1').append('<p>* ' + d.whatDescribesYourBusiness1 + '</p>');
                }
            });

            // Run the data through crossfilter and load our 'facts'
            var facts = crossfilter(data);

            // reset all button - this includes all facts
            var all = facts.groupAll();

            // reset all button - count all the facts
            dc.dataCount(".dc-data-count") 
                .dimension(facts) 
                .group(all);
            dc.dataCount(".dc-data-count2") 
                .dimension(facts) 
                .group(all);


            /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
            var ageLowerValue = facts.dimension(function (d) { 
                return d.ageLower;
            });
            var ageLowerValueGroup = ageLowerValue.group();

            var familiarDtProgram = facts.dimension(function (d) {
                if (d.familiarDtProgram == "") {
                    return "No answer";
                } else {
                    return d.familiarDtProgram;
                }
            });
            var familiarDtProgramGroup = familiarDtProgram.group();

            var yourRoleInBusiness = facts.dimension(function (d) {
                if (d.yourRoleInBusiness == "") {
                    return "No answer";
                } else {
                    return d.yourRoleInBusiness;
                }
            });
            var yourRoleInBusinessGroup = yourRoleInBusiness.group();

            var feelSafeWorkingDt = facts.dimension(function (d) {
                if (d.feelSafeWorkingDt == "") {
                    return "No answer";
                } else {
                    return d.feelSafeWorkingDt;
                }
            });
            var feelSafeWorkingDtGroup = feelSafeWorkingDt.group();

            var believeDtProgramMakesSafer = facts.dimension(function (d) {
                if (d.believeDtProgramMakesSafer == "") {
                    return "No answer";
                } else {
                    return d.believeDtProgramMakesSafer;
                }
            });
            var believeDtProgramMakesSaferGroup = believeDtProgramMakesSafer.group();

            var howEffectiveResolveBehavior = facts.dimension(function (d) {
                if (d.howEffectiveResolveBehavior == "") {
                    return "No answer";
                } else {
                    return d.howEffectiveResolveBehavior;
                }
            });
            var howEffectiveResolveBehaviorGroup = howEffectiveResolveBehavior.group();


            var everWitnessedProgramHost = facts.dimension(function (d) {
                if (d.everWitnessedProgramHost == "") {
                    return "No answer";
                } else {
                    return d.everWitnessedProgramHost;
                }
            });
            var everWitnessedProgramHostGroup = everWitnessedProgramHost.group();

            var hostApproachable = facts.dimension(function (d) {
                if (d.hostApproachable == "") {
                    return "No answer";
                } else {
                    return d.hostApproachable;
                }
            });
            var hostApproachableGroup = hostApproachable.group();

            var howOftenSeeHost = facts.dimension(function (d) {
                if (d.howOftenSeeHost == "") {
                    return "No answer";
                } else {
                    return d.howOftenSeeHost;
                }
            });
            var howOftenSeeHostGroup = howOftenSeeHost.group();

            var howOftenInteractWithPeople = facts.dimension(function (d) {
                if (d.howOftenInteractWithPeople == "") {
                    return "No answer";
                } else {
                    return d.howOftenInteractWithPeople;
                }
            });
            var howOftenInteractWithPeopleGroup = howOftenInteractWithPeople.group();

            var mostImportantAboutHosts = facts.dimension(function (d) {
                return mostImportantAboutHostsValues[d.mostImportantAboutHosts];
            });
            var mostImportantAboutHostsGroup = mostImportantAboutHosts.group();

            var opinionFirstPriorityForServices = facts.dimension(function (d) {
                if (d.opinionFirstPriorityForServices == "") {
                    return "No answer";
                } else {
                    return d.opinionFirstPriorityForServices;
                }
            });
            var opinionFirstPriorityForServicesGroup = opinionFirstPriorityForServices.group();

            var improvementsForYourSafety = facts.dimension(function (d) {
                return improvementsForYourSafetyValues[d.improvementsForYourSafety];
            });
            var improvementsForYourSafetyGroup = improvementsForYourSafety.group();

            var whatDescribesYourBusiness = facts.dimension(function (d) {
                return whatDescribesYourBusinessValues[d.whatDescribesYourBusiness];
            });
            var whatDescribesYourBusinessGroup = whatDescribesYourBusiness.group();

            var gender = facts.dimension(function (d) {
                if (d.gender == "") {
                    return "No answer";
                } else {
                    return d.gender;
                }
            });
            var genderGroup = gender.group();

            /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
            /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

            // Create dataTable dimension
            var ageDimension = facts.dimension(function (d) { 
                return d.ageLower;
            });

            // Setup the charts
            /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
            var piePercentage = function(d, sumgroup) {
                //var percent = d.data.key;
                var fraction = d.value / _.reduce(sumgroup.all(), function(memo, d){ return memo + d.value; }, 0);
                var percent = Math.round(fraction * 100);
                var phrase = "";
                if (d.data) {
                    phrase = d.data.key + "  " + percent + "%";    
                } else {
                    phrase = percent + "%";    
                }
                return phrase;
            }
            var yearsFormatter = function(d) {
                var yearText = (d == 0 ? d : d + " years");
                return yearText;
            }
            var peopleFormatter = function(d) {
                if (d > 1)
                    return d + " people";
                else if (d == 1)
                    return d + " person";
                else
                    return d;
            }
            ageLowerChart.width(264) 
                .height(220) 
                .margins({top: 5, right: 1, bottom: 20, left: 30})
                .dimension(ageLowerValue) 
                .group(ageLowerValueGroup) 
                .transitionDuration(500) 
                .centerBar(true) 
                .gap(-8)
                .x(d3.scale.linear().domain([0, 80])) 
                .filter([0, 79]) 
                .elasticY(true) 
                .xAxis()
                .tickFormat(function(d) { return yearsFormatter(d); })
                .ticks(3);

            familiarDtProgramChart.width(280) 
                .height(200) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(familiarDtProgram) 
                .group(familiarDtProgramGroup) 
                .label(function(d){return piePercentage(d, familiarDtProgramGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});

            yourRoleInBusinessChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(yourRoleInBusiness) 
                .group(yourRoleInBusinessGroup) 
                .label(function(d){return piePercentage(d, yourRoleInBusinessGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});

            feelSafeWorkingDtChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(feelSafeWorkingDt) 
                .group(feelSafeWorkingDtGroup) 
                .label(function(d){return piePercentage(d, feelSafeWorkingDtGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});

            believeDtProgramMakesSaferChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(believeDtProgramMakesSafer) 
                .group(believeDtProgramMakesSaferGroup) 
                .label(function(d){return piePercentage(d, believeDtProgramMakesSaferGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});

            howEffectiveResolveBehaviorChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(howEffectiveResolveBehavior) 
                .group(howEffectiveResolveBehaviorGroup) 
                .label(function(d){return piePercentage(d, howEffectiveResolveBehaviorGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});

            everWitnessedProgramHostChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(everWitnessedProgramHost) 
                .group(everWitnessedProgramHostGroup) 
                .label(function(d){return piePercentage(d, everWitnessedProgramHostGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});

            hostApproachableChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(hostApproachable) 
                .group(hostApproachableGroup) 
                .label(function(d){return piePercentage(d, hostApproachableGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});

            howOftenSeeHostChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(howOftenSeeHost) 
                .group(howOftenSeeHostGroup) 
                .label(function(d){return piePercentage(d, howOftenSeeHostGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});
            
            howOftenInteractWithPeopleChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(howOftenInteractWithPeople) 
                .group(howOftenInteractWithPeopleGroup) 
                .label(function(d){return piePercentage(d, howOftenInteractWithPeopleGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});

            mostImportantAboutHostsChart.width(270)
                .height(220) 
                .margins({top: 5, right: 1, bottom: 20, left: 6})
                .dimension(mostImportantAboutHosts) 
                .group(mostImportantAboutHostsGroup)
                .colors(d3.scale.category20())
                .label(function (d){
                  return d.key.split('^')[1];
                  }) 
                .title(function(d){return d.key.split('^')[1] + ", " + piePercentage(d, mostImportantAboutHostsGroup);})
                .xAxis()
                .tickFormat(function(d) { return d; })
                .ticks(4);

            opinionFirstPriorityForServicesChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(opinionFirstPriorityForServices) 
                .group(opinionFirstPriorityForServicesGroup) 
                .label(function(d){return piePercentage(d, opinionFirstPriorityForServicesGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});

            improvementsForYourSafetyChart.width(270)
                .height(860) 
                .margins({top: 5, right: 1, bottom: 20, left: 6})
                .dimension(improvementsForYourSafety) 
                .group(improvementsForYourSafetyGroup)
                .colors(d3.scale.category20())
                .label(function (d){
                  return d.key.split('^')[1];
                  }) 
                .title(function(d){return d.key.split('^')[1] + ", " + piePercentage(d, improvementsForYourSafetyGroup);})
                .xAxis()
                .tickFormat(function(d) { return d; })
                .ticks(4);

            whatDescribesYourBusinessChart.width(270)
                .height(220) 
                .margins({top: 5, right: 1, bottom: 20, left: 6})
                .dimension(whatDescribesYourBusiness) 
                .group(whatDescribesYourBusinessGroup)
                .colors(d3.scale.category20())
                .label(function (d){
                  return d.key.split('^')[1];
                  }) 
                .title(function(d){return d.key.split('^')[1] + ", " + piePercentage(d, whatDescribesYourBusinessGroup);})
                .xAxis()
                .tickFormat(function(d) { return d; })
                .ticks(4);

            genderChart.width(300) 
                .height(220) 
                .radius(100) 
                .innerRadius(30) 
                .dimension(gender) 
                .group(genderGroup) 
                .label(function(d){return piePercentage(d, genderGroup);})
                .title(function(d){return d.data.key + ", " + peopleFormatter(d.value);});

            // Render the Charts
            dc.renderAll();

        });

    </script>

</%def>

<%def name="dcCommuterSurvey()">
  <div class='row' name="dc-data-top" data-spy="affix" data-offset-top="1150" >
    <div class="dc-data-count well" style="float: left; margin-top: 0;"> 
      <span> 
          <span class="filter-count"></span>
          selected out of
          <span class="total-count"></span> 
          records | <a href="#dc-data-top" name="dc-data-count" onclick="javascript:dc.filterAll(); dc.renderAll();">Reset</a> 
      </span>
    </div>
  </div>
  <div class='row'>   
    <div class='span4' id='dc-commuteDuration-chart'>
        <h4>How much time do you spend each day commuting over the hill and back?</h4> 
    </div>
    <div class='span4' id='dc-commuteType-chart'>
      <h4>How do you get to work over the hill?
        <span>
          <a class="reset" href="#dc-data-top" onclick="javascript:commuteTypeChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4> 
    </div>
    <div class='span4' id='dc-commuteActivity-chart'>
      <h4>What do you primarily do on the bus during your commute?
        <span>
          
          <a class="reset" href="#dc-data-top" onclick="javascript:commuteActivityChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
  </div><!-- row -->
  <hr>
  <div class="row">
    <div class='span4' id='dc-employmentType-chart'>
      <h4>What is your functional employment area at your current job?
        <span>
          <a class="reset" href="#dc-data-count" onclick="javascript:employmentTypeChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a>
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-employmentDuration-chart'>
        <h4>How long have you been with your current employer?</h4> 
    </div>
    <div class='span4' id='dc-senority-chart'>
      <h4>What is your position or level of seniority?
        <span>
          <a class="reset" href="#dc-data-count" onclick="javascript:senorityChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
  </div><!-- row -->
  <hr>
  <div class="row">
    <div class='span4' id='dc-salary-chart'> 
      <h4>Salary Range
        <span>
            (drag sliders to filter results)
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-whyCommute-chart'>
      <h4>Why do you choose to work over the hill? (Pick the MOST IMPORTANT reason).
        <span>
            <br>
            <a class="reset" href="#dc-data-count" onclick="javascript:whyCommuteChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-whyLiveInSc-chart'>
      <h4>Why do you choose to live in Santa Cruz? (Pick the MOST IMPORTANT reason).
        <span>
          <br>
          <a class="reset" href="#dc-data-count" onclick="javascript:whyLiveInScChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
  </div><!-- row -->
  <hr>
  <div class="row">
    <div class='span4' id='dc-college-chart'>
      <h4>Did you go to college in Santa Cruz?
        <span>
          <br>
          <a class="reset" href="#dc-data-count" onclick="javascript:collegeChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4> 
    </div>
    <div class='span4' id='dc-residenceDuration-chart'>
      <h4>How long have you lived in Santa Cruz?
        <span>
          <br />(drag to filter results)
          <a class="reset" href="#dc-data-count" onclick="javascript:residenceDurationChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-workedInSc-chart'>
      <h4>Have you ever worked in Santa Cruz?
        <span>
            
            <a class="reset" href="#dc-data-count" onclick="javascript:workedInScChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
  </div><!-- row -->
  <hr>
  <div class="row">
    <div class='span4' id='dc-whyNotWorkInSc-chart'>
      <h4>Why did you stop working in Santa Cruz?
        <span>
          
          <a class="reset" href="#dc-data-count" onclick="javascript:whyNotWorkInScChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-salaryNeeded-chart'>
      <h4>Within what percentage of your current total compensation (salary, stock options, health and benefits, job position) would a Santa Cruz opportunity have to come for you to forgo your current job and commute?
        <span>
          
          <a class="reset" href="#dc-data-count" onclick="javascript:salaryNeededChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-heardOfStartupNewsHere-chart'>
      <h4>How much have you heard about recent start-up activity in Santa Cruz?
        <span>
          
          <a class="reset" href="#dc-data-count" onclick="javascript:heardOfStartupNewsHereChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
  </div><!-- row -->
  <hr>
  <div class="row">
    <div class='span4' id='dc-consideredJobsInSantaCruz-chart'>
      <h4>Have you considered exploring job openings with any Santa Cruz tech companies or startups?
        <span>
          <br>
          <a class="reset" href="#dc-data-count" onclick="javascript:consideredJobsInSantaCruzChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    <!--
    <div class='span4' id='dc-techEventsInSantaCruz-chart'>
      <h4>Which of the following Santa Cruz tech-community events have you attended?
        <span>
          <br>
          <a class="reset" href="#dc-data-count" onclick="javascript:techEventsInSantaCruzChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    -->
    <div class='span8' id='dc-age-chart'>
      <h4>Age of Respondents
        <span>
            (drag sliders to filter results)
        </span>
      </h4>
    </div>
  </div><!-- row -->
  <hr>
  <div class="row">
    <div class='span4' id='dc-maritalStatus-chart'>
      <h4>Marital status
        <span>
          
          <a class="reset" href="#dc-data-count" onclick="javascript:maritalStatusChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-children-chart'>
      <h4>Do you have children 17 years of age or younger living in the household?
        <span>
          
          <a class="reset" href="#dc-data-count" onclick="javascript:childrenChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
    <div class='span4' id='dc-rentOrOwn-chart'>
      <h4>Do you rent or own your home?
        <span>
          
          <a class="reset" href="#dc-data-count" onclick="javascript:rentOrOwnChart.filterAll();dc.redrawAll();" style="display: none;"> reset</a> 
        </span>
      </h4>
    </div>
  </div><!-- row -->
  <!-- removing table for now
  <hr>
   <div class='row'> 
    <div class='span12'>
      <div class='dc-data-count2'>
        <span> 
          Table listing
          <span class="filter-count"></span>
          records out of
          <span class="total-count"></span> 
          people surveyed | <a href="#dc-data-count" onclick="javascript:dc.filterAll(); dc.renderAll();">Reset</a> 
        </span>
      </div>
    </div> 
    <h4>Comments or Suggestions for improving the Santa Cruz tech-ecosystem?</h4>
    <table class='table table-hover' style="width: 100%;" id='dc-table-graph'> 
    </table>
  </div> -->
  <hr>
  <div class='row'> 
    <div class='span12' id='dc-commentsOrSuggestions-chart'>
      <h4>Comments and Suggestions</h4>
      <div id="commentsOrSuggestionsContainer">
      </div>
    </div>
  </div>

  <script src='/js/vendor/crossfilter111.min.js' type='text/javascript'></script>
  <script src='/js/vendor/dc130.min.js' type='text/javascript'></script>
  <link href='/styles/vendor/dc.css' rel='stylesheet' type='text/css'>
  
  <script>
      // Create the dc.js chart objects & link to div
      var salaryChart = dc.barChart("#dc-salary-chart");
      var commuteDurationChart = dc.lineChart("#dc-commuteDuration-chart");

      var ageChart = dc.barChart("#dc-age-chart");
      var senorityChart = dc.rowChart("#dc-senority-chart");
      
      var collegeChart = dc.rowChart("#dc-college-chart");
      var commuteTypeChart = dc.rowChart("#dc-commuteType-chart");
      var employmentDurationChart = dc.lineChart("#dc-employmentDuration-chart");

      var employmentTypeChart = dc.rowChart("#dc-employmentType-chart");
      

      var workedInScChart = dc.pieChart("#dc-workedInSc-chart");
      var whyLiveInScChart = dc.pieChart("#dc-whyLiveInSc-chart");
      var residenceDurationChart = dc.lineChart("#dc-residenceDuration-chart");
      
      var rentOrOwnChart = dc.pieChart("#dc-rentOrOwn-chart");
      var whyNotWorkInScChart = dc.pieChart("#dc-whyNotWorkInSc-chart");
      var salaryNeededChart = dc.pieChart("#dc-salaryNeeded-chart");

      var heardOfStartupNewsHereChart = dc.pieChart("#dc-heardOfStartupNewsHere-chart");
      var consideredJobsInSantaCruzChart = dc.pieChart("#dc-consideredJobsInSantaCruz-chart");
      var techEventsInSantaCruzChart = dc.pieChart("#dc-techEventsInSantaCruz-chart");

      var maritalStatusChart = dc.pieChart("#dc-maritalStatus-chart");
      var childrenChart = dc.pieChart("#dc-children-chart");
      var whyCommuteChart = dc.pieChart("#dc-whyCommute-chart");
      var commuteActivityChart = dc.pieChart("#dc-commuteActivity-chart");

      //var dataTable = dc.dataTable("#dc-table-graph");

      var data = null;
      
      // NOTE: the csv file's fields tend to get wrapped in apostrophes thanks to open office:
      // ( "field", "field", .. )
      //   remove these or the csv loader here won't work e.g.: ( field, field, .. )
      d3.csv("/surveys/techCommuterSurvey6.csv", function(error, data) {
          //console.log(error);
          //console.log(data);
          /*
              <th>Commute Duration</th>             commuteDuration 
              <th>Commute Type</th>                 travelType
              <th>Commute Activity</th>             commuteActivity 
              <th>Employment Type</th>              employmentType  
              <th>Years at Job</th>                 employmentDuration  
              <th>Seniority</th>                    employmentLevel
              <th>Salary</th>                       salary
              <th>Why Commute</th>                  whyCommute
              <th>Why Live Here</th>                whyLiveHere 
              <th>College in Santa Cruz</th>        collegeInSantaCruz  
              <th>Residence Duration</th>           residenceDuration 
              <th>Worked in Santa Cruz</th>         workedInSantaCruz 
              <th>Why not work in Santa Cruz</th>   whyNoWorkInSantaCruz  
              <th>Salary needed to work here</th>   whatSalaryNeeded  
              <th>Children</th>                     children  
              <th>Rent or own</th>                  rentOrOwn 
              <th>Age</th>                          age
          */

          data.forEach(function(d) {
              d.commuteDuration = +d.commuteDuration/60;
              d.employmentDuration = +d.employmentDuration;
              d.salary = +d.salary;
              d.residenceDuration = +d.residenceDuration;
              d.age = +d.age;
              if (d.commentsOrSuggestions != "(blank)") {
                  $('#commentsOrSuggestionsContainer').append('<p>* ' + d.commentsOrSuggestions + '</p>');
              }
          });

          // Run the data through crossfilter and load our 'facts'
          var facts = crossfilter(data);

          // reset all button - this includes all facts
          var all = facts.groupAll();

          // reset all button - count all the facts
          dc.dataCount(".dc-data-count") 
              .dimension(facts) 
              .group(all);
          // note: code for table
          //dc.dataCount(".dc-data-count2") 
          //    .dimension(facts) 
          //    .group(all);


          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var salaryValue = facts.dimension(function (d) { 
              return d.salary;
          });
          var salaryValueGroup = salaryValue.group();

          var commuteDurationValue = facts.dimension(function (d) { 
              return d.commuteDuration;
          });
          var commuteDurationValueGroup = commuteDurationValue.group();
              //.reduceCount(function(d) { return d.commuteDuration; }) // counts

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var ageValue = facts.dimension(function (d) { 
              return d.age;
          });
          var ageValueGroup = ageValue.group()
              .reduceCount(function(d) { return d.age; }) // counts

          var senorityValue = facts.dimension(function (d) {
              //console.log("college: " + d.collegeWhere)
              switch (d.employmentLevel) {
                  case 'C-Level Executive': return "1.C-Level Executive";
                  case 'Consultant': return "2.Consultant";
                  case 'Director': return "3.Director";
                  case 'Independent Contractor': return "4.Independent Contractor";
                  case 'Intern': return "5.Intern";
                  case 'Team Manager': return "6.Team Manager";
                  case 'Team Member': return "7.Team Member";
                  case 'Vice President': return "8.Vice President";
                  default: return "0.No answer";
              } 
          });
          var senorityValueGroup = senorityValue.group();

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var collegeValue = facts.dimension(function (d) {
              //console.log("college: " + d.collegeWhere)
              switch (d.collegeWhere) {
                  case 'UCSC': return "0.UCSC";
                  case 'Cabrillo': return "1.Cabrillo";
                  default: return "2.No answer";
              } 
          });
          var collegeValueGroup = collegeValue.group();

          var commuteType = facts.dimension(function (d) {
              switch (d.travelType) {
                  case 'Company bus': return "0.Company bus";
                  case 'Car (single occupancy)': return "1.Car (single occupancy)";
                  case 'Independent shuttle': return "2.Independent shuttle";
                  case 'Carpool': return "3.Carpool";
                  default: return "4.No answer";
              } 
          });
          var commuteTypeGroup = commuteType.group();

          var employmentDuration = facts.dimension(function (d) { 
              return d.employmentDuration;
          });
          var employmentDurationGroup = employmentDuration.group()
              .reduceCount(function(d) { return d.employmentDuration; }) // counts

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var employmentType = facts.dimension(function (d) {
              //console.log("college: " + d.collegeWhere)
              switch (d.employmentType) {
                  case '(blank)': return "0.No answer";
                  case 'Bio Engineer': return "1.Bio Engineer";
                  case 'Business Development': return "2.Business Development";
                  case 'Design': return "3.Design";
                  case 'Education': return "4.Education";
                  case 'Electrical Engineer': return "5.Electrical Engineer";
                  case 'Executive': return "6.Executive";
                  case 'Finance': return "7.Finance";
                  case 'Hardware QA': return "8.Hardware QA";
                  case 'IT': return "9.IT";
                  case 'Legal': return "10.Legal";
                  case 'Management': return "11.Management";
                  case 'Manufacturing': return "12.Manufacturing";
                  case 'Marketing': return "13.Marketing";
                  case 'Mechanical Engineer': return "14.Mechanical Engineer";
                  case 'Operations': return "15.Operations";
                  case 'Recruiter': return "16.Recruiter";
                  case 'Sales': return "17.Sales";
                  case 'Software Developer': return "18.Software Developer";
                  case 'Support Engineer': return "19.Technical Support";
                  case 'Technical Support': return "19.Technical Support";
                  case 'Technical Writer': return "19.Technical Support";
                  case 'Engineering (other)': return "19.Enginering (other)";
                  case 'Other': return "19.Other";
                  default: return "0.No answer";
              } 
          });
          var employmentTypeGroup = employmentType.group();

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var workedInSc = facts.dimension(function (d) {
              if (d.workedInSantaCruz == "(blank)") {
                  return "No answer";
              } else {
                  return d.workedInSantaCruz;
              }
          });
          var workedInScGroup = workedInSc.group();

          var whyLiveInSc = facts.dimension(function (d) {
              if (d.whyLiveHere == "(blank)") {
                  return "No answer";
              } else {
                  return d.whyLiveHere;
              }
          });
          var whyLiveInScGroup = whyLiveInSc.group();

          var residenceDuration = facts.dimension(function (d) { 
              if (d.residenceDuration == "(blank)") {
                  return 0;
              } else {
                  return d.residenceDuration;
              }
          });
          residenceDurationGroup = residenceDuration.group()
              .reduceCount(function(d) { return d.residenceDuration; }) // counts

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var rentOrOwn = facts.dimension(function (d) {
              if (d.rentOrOwn == "(blank)") {
                  return "No answer";
              } else {
                  return d.rentOrOwn;
              }
          });
          var rentOrOwnGroup = rentOrOwn.group();

          var whyNotWorkInSc = facts.dimension(function (d) {
              if (d.whyNoWorkInSantaCruz == "(blank)") {
                  return "No answer";
              } else {
                  return d.whyNoWorkInSantaCruz;
              }
          });
          var whyNotWorkInScGroup = whyNotWorkInSc.group();

          var salaryNeeded = facts.dimension(function (d) {
              if (d.whatSalaryNeeded == "(blank)") {
                  return "No answer";
              } else {
                  return d.whatSalaryNeeded;
              }
          });
          var salaryNeededGroup = salaryNeeded.group();

          var heardOfStartupNewsHere = facts.dimension(function (d) {
              if (d.heardOfStartupNewsHere == "(blank)") {
                  return "No answer";
              } else {
                  return d.heardOfStartupNewsHere;
              }
          });
          var heardOfStartupNewsHereGroup = heardOfStartupNewsHere.group();

          var consideredJobsInSantaCruz = facts.dimension(function (d) {
              if (d.consideredJobsInSantaCruz == "(blank)") {
                  return "No answer";
              } else {
                  return d.consideredJobsInSantaCruz;
              }
          });
          var consideredJobsInSantaCruzGroup = consideredJobsInSantaCruz.group();

          var techEventsInSantaCruz = facts.dimension(function (d) {
              if (d.techEventsInSantaCruz == "(blank)") {
                  return "Have not attended an event";
              } else {
                  return d.techEventsInSantaCruz;
              }
          });
          var techEventsInSantaCruzGroup = techEventsInSantaCruz.group();

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var children = facts.dimension(function (d) {
              if (d.children == "(blank)") {
                  return "No answer";
              } else {
                  return d.children;
              }
          });
          var childrenGroup = children.group();

          var maritalStatus = facts.dimension(function (d) {
              if (d.maritalStatus == "(blank)") {
                  return "No answer";
              } else {
                  return d.maritalStatus;
              }
          });
          var maritalStatusGroup = maritalStatus.group();

          var whyCommute = facts.dimension(function (d) {
              if (d.whyCommute == "(blank)") {
                  return "No answer";
              } else {
                  return d.whyCommute;
              }
          });
          var whyCommuteGroup = whyCommute.group();

          var commuteActivity = facts.dimension(function (d) {
              if (d.commuteActivity == "(blank)") {
                  return "Not a bus commuter";
              } else {
                  return d.commuteActivity;
              }
          });
          var commuteActivityGroup = commuteActivity.group();

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

          // Create dataTable dimension
          var commuteDurationDimension = facts.dimension(function (d) { 
            return d.commuteDuration;
          });

          // Setup the charts
          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var commasFormatter = d3.format(",.0f");
          salaryChart.width(280) 
              .height(150) 
              .margins({top: 10, right: 10, bottom: 20, left: 60}) 
              .dimension(salaryValue) 
              .group(salaryValueGroup) 
              .transitionDuration(500) 
              .centerBar(true) 
              .gap(-8)
              .x(d3.scale.linear().domain([0, 510000])) 
              .filter([0, 505000])
              .elasticY(true) 
              .xAxis()
              .tickFormat(function(d) { return "$" + commasFormatter(d); })
              .ticks(6);

          var hoursFormatter = function(d) {
            if (d > 1)
                return d + "hrs";
            else
                return d + " hour";
          }
          // bar chart of commute duration and its sum of occurences
          commuteDurationChart.width(370) 
              .height(150) 
              .margins({top: 10, right: 10, bottom: 20, left: 60}) 
              .dimension(commuteDurationValue) 
              .group(commuteDurationValueGroup) 
              .transitionDuration(500)
              .title(function(d){
                  return d.key
                  + " hrs \nNumber of Commuters: " + d.value; 
                  })
              .x(d3.scale.linear().domain([0.5,6.5]))
              .elasticY(true) 
              .filter([0.6, 5.1])
              .xAxis()
              .tickFormat(function(d) { return hoursFormatter(d); })
              .ticks(6);

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          var yearsFormatter = function(d) {
              return d + " years";
          }
          // age graph
          ageChart.width(400) 
              .height(220) 
              .margins({top: 10, right: 10, bottom: 20, left: 40}) 
              .dimension(ageValue) 
              .group(ageValueGroup) 
              .transitionDuration(500) 
              .centerBar(true) 
              .gap(-6)
              .elasticY(true) 
              .filter([0, 71]) 
              .x(d3.scale.linear().domain((d3.extent(data, function(d) { return d.age + 2; }))))
              .xAxis()
              .tickFormat(function(d) { return yearsFormatter(d); });

          var peopleFormatter = function(d) {
            if (d > 1)
                return d + " people";
            else if (d == 1)
                return d + " person";
            else
                return d;
          }

          senorityChart.width(400) 
              .height(250) 
              .dimension(senorityValue) 
              .group(senorityValueGroup)
              .colors(d3.scale.category20b())
              .label(function (d){
                  return d.key.split(".")[1];
                  }) 
              .title(function(d){return d.value + " commuters";})
              .xAxis()
              .tickFormat(function(d) { return peopleFormatter(d); })
              .ticks(4);

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          collegeChart.width(200) 
              .height(220) 
              .margins({top: 15, left: 15, right: 15, bottom: 15}) 
              .dimension(collegeValue) 
              .group(collegeValueGroup) 
              .colors(d3.scale.category20c())
              .label(function (d){
                  return d.key.split(".")[1];
                  })
              .title(function(d){return d.value + " commuters";}) 
              .xAxis()
              .tickFormat(function(d) { return d; })
              .ticks(3);

          commuteTypeChart.width(200) 
              .height(250) 
              .margins({top: 15, left: 15, right: 15, bottom: 15}) 
              .dimension(commuteType) 
              .group(commuteTypeGroup)
              .colors(d3.scale.category20b())
              .label(function (d){
                  return d.key.split(".")[1];
                  }) 
              .title(function(d){return d.value + " commuters";})
              .xAxis()
              .tickFormat(function(d) { return d; })
              .ticks(3);

          employmentDurationChart.width(290) 
              .height(248) 
              .margins({top: 40, right: 10, bottom: 20, left: 60}) 
              .dimension(employmentDuration) 
              .group(employmentDurationGroup) 
              .transitionDuration(500)
              .elasticY(true)
              .x(d3.scale.linear().domain([0,12.5]))
              .filter([0, 12.1])
              .xAxis()
              .ticks(4)
              .tickFormat(function(d) { return yearsFormatter(d); });

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          employmentTypeChart.width(220) 
              .height(300) 
              .margins({top: 5, left: 5, right: 10, bottom: 40}) 
              .dimension(employmentType) 
              .group(employmentTypeGroup) 
              .colors(d3.scale.category20c())
              .label(function (d){
                  return d.key.split(".")[1];
                  }) 
              .title(function(d){return d.value + " commuters.";})
              .xAxis()
              .ticks(4);

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          // pie chart section begins here
          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          workedInScChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(workedInSc) 
              .group(workedInScGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});


          whyLiveInScChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(whyLiveInSc) 
              .group(whyLiveInScGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          residenceDurationChart.width(280) 
              .height(220) 
              .margins({top: 10, right: 10, bottom: 20, left: 60}) 
              .dimension(residenceDuration) 
              .group(residenceDurationGroup) 
              .transitionDuration(500)
              .elasticY(true) 
              .x(d3.scale.linear().domain([0,12.3]))
              .filter([0, 12.2]) 
              .xAxis()
              .ticks(4)
              .tickFormat(function(d) { return yearsFormatter(d); });

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          rentOrOwnChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(rentOrOwn) 
              .group(rentOrOwnGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          whyNotWorkInScChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(whyNotWorkInSc) 
              .group(whyNotWorkInScGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          salaryNeededChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(salaryNeeded) 
              .group(salaryNeededGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          heardOfStartupNewsHereChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(heardOfStartupNewsHere) 
              .group(heardOfStartupNewsHereGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          techEventsInSantaCruzChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(techEventsInSantaCruz) 
              .group(techEventsInSantaCruzGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          consideredJobsInSantaCruzChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(consideredJobsInSantaCruz) 
              .group(consideredJobsInSantaCruzGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
          maritalStatusChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(maritalStatus) 
              .group(maritalStatusGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});  

          childrenChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(children) 
              .group(childrenGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          whyCommuteChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(whyCommute) 
              .group(whyCommuteGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          commuteActivityChart.width(300) 
              .height(220) 
              .radius(100) 
              .innerRadius(30) 
              .dimension(commuteActivity) 
              .group(commuteActivityGroup) 
              .title(function(d){return d.data.key + ", " + d.value;});

          // Table of commuter survey data
          //dataTable.width(760).height(800) 
          //    .dimension(commuteDurationDimension)
          //        .group(function(d) { return ''})
          //    .columns([
          //        function(d) { return commentsOrSuggestionsFormatter(d.commentsOrSuggestions); },
          //    ])
          //    .sortBy(function(d){ 
          //        return d.commuteDuration; 
          //    })
          //    .order(d3.ascending);

          // Render the Charts
          dc.renderAll();

      });

  </script>

</%def>


<%def name="constancyChart(constancyData, chart, typeName, barColor, barHover)">

<style>

  #${chart} .${chart}bar rect {
    fill: ${barColor};
  }

  #${chart} .${chart}bar:hover rect {
    fill: ${barHover};
  }

  #${chart} a:hover {
    fill:#D15D00;
  }

  #${chart} a {
    font-size: 1.3em;
  }

  .value {
    fill: white;
  }

  .axis {
    shape-rendering: crispEdges;
  }

  .axis path {
    fill: none;
    stroke: none;
  }

  .x.axis line {
    stroke: #eee;
    stroke-opacity: .8;
  }

  .y.axis path {
    stroke: black;
  }


</style>


<p id="${chart}menu">
  <b>Top ${typeName} by various counts</b><br>Compare by: 
  <select></select>
</p>
<div id="${chart}">
</div>

<script>

  var margin = {
      top: 20, 
      right: 500, 
      bottom: 20, 
      left: 40
    }; 

  data = ${constancyData | n}

  var ${chart}barHeight = 28;
  var ${chart}totalHeight = ${chart}barHeight * data.length;
  
  var width = 960 - margin.left - margin.right;
  var ${chart}height = ${chart}totalHeight + margin.top + margin.bottom;

  var format = d3.format("d");
  var ${chart}states;
  var age;

  var ${chart}x = d3.scale.linear()
      .range([0, width]);

  var ${chart}y = d3.scale.ordinal()
      .rangeRoundBands([0, ${chart}height], .1);

  var ${chart}xAxis = d3.svg.axis()
      .scale(${chart}x)
      .orient("top")
      .tickSize(-${chart}height - margin.bottom)
      .tickFormat(format);

  var ${chart}svg = d3.select("#${chart}").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", ${chart}height + margin.top + margin.bottom)
      .style("margin-left", -margin.left + "px")
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  ${chart}svg.append("g")
      .attr("class", "x axis");
  
  ${chart}svg.append("g")
      .attr("class", "y axis")
    .append("line")
      .attr("class", "domain")
      .attr("y2", ${chart}height);

  var ${chart}menu = d3.select("#${chart}menu select")
      .on("change", ${chart}change);

  ${chart}states = data;
  
  var ${chart}ages = d3.keys(${chart}states[0]).filter(function(key) {
    return key != "views" && key != "code" && key != "title" && key != "url" && key != "totalVotes" && key != "yesPercent";
  });


  ${chart}menu.selectAll("option")
      .data(${chart}ages)
    .enter().append("option")
      .text(function(d) { return d; });

  ${chart}menu.property("value", "Total Views");

  ${chart}redraw();
  

  var altKey;

  d3.select(window)
      .on("keydown", function() { altKey = d3.event.altKey; })
      .on("keyup", function() { altKey = false; });

  function ${chart}change() {

    d3.transition()
        .duration(altKey ? 4000 : 1500)
        .each(${chart}redraw);
  }

  function ${chart}redraw() {
    var age1 = ${chart}menu.property("value");
    var top = ${chart}states.sort(function(a, b) { return b[age1] - a[age1]; });

    ${chart}y.domain(top.map(function(d) { return d.code; }));

    var ${chart}bar = ${chart}svg.selectAll(".${chart}bar")
        .data(top, function(d) { return d.code; });

    var ${chart}barEnter = ${chart}bar.enter().insert("g", ".axis")
        .attr("class", "${chart}bar")
        .attr("transform", function(d) { return "translate(0," + (${chart}y(d.code) + ${chart}height) + ")"; })
        .style("fill-opacity", 0);

    ${chart}barEnter
        .append("rect")
        .attr("width", age && function(d) { return ${chart}x(d[age]); })
        .attr("height", ${chart}y.rangeBand());

    ${chart}barEnter.append("a") 
        .attr("xlink:href", function(d) {
          return d.url
        })
        .attr("class", "listed-item-title data-label")
        .append("text")
        .attr("x", width + 5)
        .attr("y", ${chart}y.rangeBand() / 2)
        .attr("dy", ".35em")
        .attr("text-anchor", "start")
        .text(function(d) { return d.title; });

    ${chart}barEnter.append("text")
        .attr("class", "value")
        .attr("x", age && function(d) { return ${chart}x(d[age]) - 3; })
        .attr("y", ${chart}y.rangeBand() / 2)
        .attr("dy", ".35em")
        .attr("text-anchor", "end");

    ${chart}x.domain([0, top[0][age = age1]]);

    var ${chart}barUpdate = d3.transition(${chart}bar)
        .attr("transform", function(d) { return "translate(0," + (d.y0 = ${chart}y(d.code)) + ")"; })
        .style("fill-opacity", 1);

    ${chart}barUpdate.select("rect")
        .attr("width", function(d) { return ${chart}x(d[age]); });

    ${chart}barUpdate.select(".value")
        .attr("x", function(d) { return ${chart}x(d[age]) - 3; })
        .text(function(d) { return format(d[age]); });

    var ${chart}barExit = d3.transition(${chart}bar.exit())
        .attr("transform", function(d) { return "translate(0," + (d.y0 + ${chart}height) + ")"; })
        .style("fill-opacity", 0)
        .remove();

    ${chart}barExit.select("rect")
        .attr("width", function(d) { return ${chart}x(d[age]); });

    ${chart}barExit.select(".value")
        .attr("x", function(d) { return ${chart}x(d[age]) - 3; })
        .text(function(d) { return format(d[age]); });

    d3.transition(${chart}svg).select(".x.axis")
        .call(${chart}xAxis);
  }

</script>

</%def>

<%def name="barChart(barData, chart, views, votes, downs, barText)">
  <style>
    #${chart} rect.views{
      fill: ${views};
    }

    #${chart} rect.totalVotes{
      fill: ${votes};
    }
    
    #${chart} rect.downVotes{
      fill: ${downs};
    }

    #${chart} text.views {
      fill: ${barText};
      font: 10px sans-serif;
      text-anchor: end;
    }

    #${chart} text.totalVotes {
      fill: white;
      font: 10px sans-serif;
      text-anchor: end;
    }

    #${chart} text.downVotes {
      fill: white;
      font: 10px sans-serif;
      text-anchor: end;
    }

    #${chart} .title { 
      font-size: 14px; 
      font-weight: bold; 
      fill: black;
    }

  </style>

  <svg id="${chart}"></svg>

  <script src="http://d3js.org/d3.v3.min.js"></script>
  <script>

    var margin = {
      top: 15, 
      right: 300, 
      bottom: 15, 
      left: 35
    }; 
    var width = 900 - margin.left - margin.right;
    var height = 600 - margin.top - margin.bottom;
    var barHeight = 20;

    var x = d3.scale.linear()
        .range([0, width]);

    var data = ${barData | n}

    var dataViews = function(d) { return d.views; };
    var dataVotes = function(d) { return d.totalVotes; };

    var viewScale = d3.scale.linear()
      .domain([0, d3.max(data, dataViews)])
      .range([0, width]);
    // if I give votes the same width scale as views I may be able to display them as a stacked bar group
    // worth a try, if I can get this working 
    var totalVoteScale = d3.scale.linear()
      .domain([0, d3.max(data, dataVotes)])
      .range([0, width]);

    var chart = d3.select("#${chart}")
        .attr("width", width + margin.left + margin.right);
    

    x.domain([0, d3.max(data, function(d) { return d.views; })]);

    chart.attr("height", barHeight * data.length + margin.top + margin.bottom);

    var bar = chart.selectAll("g")
        .data(data)
      .enter().append("g")
        .attr("transform", function(d, i) { return "translate(" + margin.left + "," + i * barHeight + ")"; });

    bar.append("rect")
          .attr("x", 0)
          .attr("width", function(d) { return x(d.views); })
          .attr("class", "views")
          .attr("height", barHeight - 1);

    bar.append("text")
          .attr("x", function(d) { return x(d.views) - 3; })
          .attr("y", barHeight / 2)
          .attr("dy", ".35em")
          .attr("class", "views")
          .text(function(d) { return d.views; });

    bar.append("rect")
          .attr("x", 0)
          .attr("width", function(d) { return x(d.totalVotes); })
          .attr("class", "totalVotes")
          .attr("height", (7 * barHeight / 8));

    bar.append("text")
          .attr("x", function(d) { return x(d.totalVotes) - 3; })
          .attr("y", barHeight / 2)
          .attr("dy", ".35em")
          .attr("class", "totalVotes")
          .text(function(d) { return d.totalVotes; });

    bar.append("rect")
          .attr("x", 0)
          .attr("width", function(d) { return x(d.downVotes); })
          .attr("class", "downVotes")
          .attr("height", (3 * barHeight / 4));

    bar.append("text")
          .attr("x", function(d) { return x(d.downVotes) - 3; })
          .attr("y", barHeight / 2)
          .attr("dy", ".35em")
          .attr("class", "downVotes")
          .text(function(d) { return d.downVotes; });

    bar.append("text")
        .attr("x", width + 5)
        .attr("y", barHeight / 2)
        .attr("dy", ".35em")
        .attr("class", "title")
        .style("text-anchor", "start")
        .text(function(d) { return d.title; });

    function type(d) {
      d.views = +d.views; // coerce to number
      return d;
    }

  </script>

</%def>

<%def name="bulletChart(bulletData)">

  <style>

    .bullet { font: 10px sans-serif; } 
    .bullet .marker { stroke: #000; stroke-width: 2px; } 
    .bullet .tick line { stroke: #666; stroke-width: .5px; } 
    .bullet .range.s0 { fill: #eee; } 
    .bullet .range.s1 { fill: #ddd; } 
    .bullet .range.s2 { fill: #ccc; } 
    .bullet .measure.s0 { fill: steelblue; } 
    .bullet .title { font-size: 14px; font-weight: bold; } 
    .bullet .subtitle { fill: #999; }

  </style> 

  <script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
  <script src="/d3/bullet.js"></script>

  <div>
    <p id='link' class='ideaListingTitle'>
      &nbsp;
    </p>
  </div>
  <button>Update</button>
  <div id="bulletChart">
  </div>
  
  <script>
    var margin = {
      top: 15, 
      right: 400, 
      bottom: 15, 
      left: 15
    }; 
    var width = 1000 - margin.left - margin.right;
    var height = 60 - margin.top - margin.bottom;

    var chart = d3.bullet() 
      .width(width)
      .height(height);

    var data = ${bulletData | n}

    var svg = d3.select("#bulletChart")
      .selectAll("svg")
        .data(data) 
      .enter().append("svg")
        .attr("class", "bullet") 
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom) 
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")") 
        .call(chart);

    var titlePlacement = width + 5;

    var title = svg.append("g") 
      .style("text-anchor", "start") 
      .attr("transform", "translate(" + titlePlacement + "," + height / 2 + ")");

    title.append("text") 
      .attr("class", "title") 
      .text(function(d) { return d.title; });

    title.append("text") 
      .attr("class", "subtitle") 
      .attr("dy", "1em") 
      .text(function(d) { return d.subtitle; });

    d3.selectAll("button").on("click", function() { 
      svg.datum(randomize).call(chart.duration(1000));
    });

    function randomize(d) { 
      if (!d.randomizer) d.randomizer = randomizer(d); 
      d.markers = d.markers.map(d.randomizer); 
      d.measures = d.measures.map(d.randomizer); 
      return d;
    }

    function randomizer(d) { 
      var k = d3.max(d.ranges) * .2; 
      return function(d) {
        return Math.max(0, d + k * (Math.random() - .5));
      }
    };

  </script>

</%def>

<%def name="newGraph(newData)">

  <style>

    path { 
      stroke: steelblue; 
      stroke-width: 2; 
      fill: none;
    }

    .axis path, .axis line {
      fill: none; 
      stroke: grey; 
      stroke-width: 1; 
      shape-rendering: crispEdges;
    }

    path {
      stroke: steelblue;
      stroke-width: 2;
      fill: none;
    }

    .grid .tick { 
      stroke: lightgrey; 
      opacity: 0.7;
    } 

    .grid path {
      stroke-width: 0;
    }

    .area { 
      fill: lightsteelblue; 
      stroke-width: 0;
    }

    text.shadow { 
      stroke: white;
      stroke-width: 2.5px; 
      opacity: 0.9;
    }

    div.tooltip { 
      position: absolute; 
      text-align: center; 
      width: 7em; 
      height: 4.5em; 
      padding: 0.4em; 
      font: 1em sans-serif; 
      background: lightsteelblue; 
      border: 0px; 
      border-radius: 0.6em; 
      pointer-events: none;
    }

  </style>

  <div>
    <p id='link' class='ideaListingTitle'>
      &nbsp;
    </p>
  </div>
  <div id="newChart">
    <!--<div id="option"> 
      <input name="updateButton" type="button" value="Update" onclick="updateData()"/>
    </div>-->
  </div>

  <script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
  <script>
    var margin = {
      top: 46, 
      right: 200, 
      bottom: 100, 
      left: 60
    }; 
    var width = 1050 - margin.left - margin.right;
    var height = 496 - margin.top - margin.bottom;

    var voteColors = {
      zero: "darkorchid",
      one: "mediumslateblue",
      aboveOne: "yellow",
      aboveQuarter: "deepskyblue",
      aboveHalf: "cyan",
      aboveThreeQuarters: "lime"
    }

    // expecting date to arrive in standard msql format
    var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;
    
    var x = d3.time.scale().range([0, width]);
    
    var y = d3.scale.linear().range([height, 0]); 
    
    var xAxis = d3.svg.axis().scale(x)
      .orient("bottom").ticks(10)
      .tickFormat(d3.time.format("%m/%d/%y")); 

    var yAxis = d3.svg.axis().scale(y)
      .orient("left").ticks(5);

    function make_x_axis() { 
      return d3.svg.axis()
        .scale(x) 
        .orient("bottom") 
        .ticks(5)
    }
    
    function make_y_axis() { 
      return d3.svg.axis()
        .scale(y) 
        .orient("left") 
        .ticks(10)
    }


    var valueline = d3.svg.line()
      .x(function(d) { return x(parseDate(d.date)); }) 
      .y(function(d) { return y(+d.views); });

    var svg = d3.select("#newChart") 
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom) 
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    // Get the data - in this case it's json in a variable
    var graphData = ${newData | n}
    //console.log(graphData);

    // Scale the range of the data
    var maxViews = d3.max(graphData, function(d) { return +d.views; });
    var maxVotes = d3.max(graphData, function(d) { return +d.totalVotes; });
    x.domain(d3.extent(graphData, function(d) { return parseDate(d.date); })); 
    y.domain([0, maxViews]);
    
    svg.append("g") 
      .attr("class", "grid") 
      .attr("transform", "translate(0," + height + ")") 
      .call(make_x_axis()
        .tickSize(-height, 0, 0) 
        .tickFormat("")
      )
    
    svg.append("g") 
      .attr("class", "grid") 
      .call(make_y_axis()
        .tickSize(-width, 0, 0) 
        .tickFormat("")
      )

    /*
    svg.append("path")  // Add the valueline path.
      .attr("class", "line")
      .attr("d", valueline(graphData));
    */

    var ttDiv = d3.select("#newChart")
      .append("div") 
      .attr("class", "tooltip") 
      .style("opacity", 0);

    function approval(u,t) {
      //console.log(t + " " + u);
      if (+t > 0) {
        var approval = Math.ceil(u/t)*100;
        return approval+"% approval <br/>";
      } else {
        return "";
      }
    }
    
    function popular(u,t) {
      if (+t > 0) {
        var score = Math.ceil(u/t)*100;
        if (score>50) {
          return true;
        } else {
          return false;
        }
      } else {
        return false;
      }
    }

    var linkDiv = d3.select("#link")

    svg.selectAll("dot") 
        .data(graphData)
      .enter().append("a") 
        .attr("xlink:href", function(d) {
          return d.url
        })
        .append( "circle" )
        .attr("r", function(d) {
          if (popular(d.upVotes, d.totalVotes)) {
            return 6;
          } else {
            return 3;
          }
        })
        .attr("cx", function(d) { return x(parseDate(d.date)); })
        .attr("cy", function(d) { return y(+d.views); })
        .style("fill", function(d) {
          if (+d.totalVotes > 3*maxVotes/4) {
            return voteColors.aboveThreeQuarters;
          } else if (+d.totalVotes > maxVotes/2) {
            return voteColors.aboveHalf;
          } else if (+d.totalVotes > maxVotes/4) {
            return voteColors.aboveQuarter;
          } else if (+d.totalVotes > 1) {
            return voteColors.aboveOne;
          } else if (+d.totalVotes > 0) {
            return voteColors.one;
          } else {
            return voteColors.zero;
          }
        })
        .style("stroke", function(d) {
          if (+d.totalVotes > maxVotes/4) {
            return "grey";
          } else {
            return "lavender";
          }
        })
        //.on("click", function(d) {
        //  linkDiv.html("<a href='" + d.url + "'>" + d.title + "</a>")
        //})
        .on("mouseover", function(d) {          
          linkDiv.html('<a href="' + d.url + '" class="listed-item-title">' + d.title + '</a>')
          ttDiv.transition() 
            .duration(200)
            .style("opacity", .9); 
          ttDiv.html(d.type + "<br/>" + d.totalVotes + " votes" + "<br/>" + approval(d.upVotes, d.totalVotes) + d.views + " views")
            .style("left", (d3.event.pageX) + "px") 
            .style("top", (d3.event.pageY - 58) + "px")
            .style("pointer-events", "none");
        }) 
        .on("mouseout", function(d) {
          ttDiv.transition() 
            .duration(500)
            .style("opacity", 0);
        });

    svg.append("g") // Add the X Axis 
      .attr("class", "x axis") 
      .attr("transform", "translate(0," + height + ")") 
      .call(xAxis)
      .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", function(d) {
            return "rotate(-35)"
        });

    svg.append("g") 
      .attr("class", "y axis") 
      .call(yAxis);

    // text label for the x axis
    svg.append("text")  
      .attr("transform", "translate(" + (width / 2) + " ," + (height + 3*margin.bottom/4) + ")")
      .style("text-anchor", "middle") 
      .text("Last Activity");

    svg.append("text") 
      .attr("transform", "rotate(-90)") 
      .attr("y", 0 - margin.left)
      .attr("x", 0 - (height / 2)) 
      .attr("dy", "1em") 
      .style("text-anchor", "middle") 
      .text("# of Views");
    
    svg.append("text") 
      .attr("x", (width / 2)) 
      .attr("y", 0 - (margin.top / 2)) 
      .attr("text-anchor", "middle") 
      .style("font-size", "16px") 
      .style("text-decoration", "underline")
      .attr("class", "shadow")
      .text("All Activities");

    svg.append("text") 
      .attr("x", (width / 2)) 
      .attr("y", 0 - (margin.top / 2)) 
      .attr("text-anchor", "middle") 
      .style("font-size", "16px") 
      .style("text-decoration", "underline") 
      .text("All Activities");

    // legend
    /*var voteColors = {
      zero: "darkorchid",
      one: "mediumslateblue",
      aboveOne: "yellow",
      aboveQuarter: "deepskyblue",
      aboveHalf: "cyan",
      aboveThreeQuarters: "lime"
    }*/
    
    var boxSpacing = 105;

    var lineSpaceMultiplier = 1.3;

    svg.append("text") 
      .attr("x", width)
      .attr("dx", "3em")
      .attr("y", "0.8em")
      .style("font-size", "16px") 
      .style("text-anchor", "start") 
      .style("text-decoration", "underline")
      .text("Legend");

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (2 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "14px") 
      .style("text-anchor", "start") 
      .text("Most votes: ");

    svg.append("rect")
      .attr("x", width + boxSpacing)
      .attr("y", (2 * lineSpaceMultiplier) + "em")
      .attr("height", "1em") 
      .attr("width", "2em")
      .style("fill", voteColors.aboveThreeQuarters)
      .style("stroke", "grey")

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (3 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "14px") 
      .style("text-anchor", "start") 
      .text("Many votes: ");

    svg.append("rect")
      .attr("x", width + boxSpacing)
      .attr("y", (3 * lineSpaceMultiplier) + "em")
      .attr("height", "1em") 
      .attr("width", "2em")
      .style("fill", voteColors.aboveHalf)
      .style("stroke", "grey")

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (4 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "14px") 
      .style("text-anchor", "start") 
      .text("Some votes: ");

    svg.append("rect")
      .attr("x", width + boxSpacing)
      .attr("y", (4 * lineSpaceMultiplier) + "em")
      .attr("height", "1em") 
      .attr("width", "2em")
      .style("fill", voteColors.aboveQuarter)
      .style("stroke", "grey")

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (5 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "14px") 
      .style("text-anchor", "start") 
      .text("Above 1 vote: ");

    svg.append("rect")
      .attr("x", width + boxSpacing)
      .attr("y", (5 * lineSpaceMultiplier) + "em")
      .attr("height", "1em") 
      .attr("width", "2em")
      .style("fill", voteColors.aboveOne)
      .style("stroke", "lavender")

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (6 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "14px") 
      .style("text-anchor", "start") 
      .text("One vote: ");

    svg.append("rect")
      .attr("x", width + boxSpacing)
      .attr("y", (6 * lineSpaceMultiplier) + "em")
      .attr("height", "1em") 
      .attr("width", "2em")
      .style("fill", voteColors.one)
      .style("stroke", "lavender")

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (7 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "14px") 
      .style("text-anchor", "start") 
      .text("Zero votes: ");

    svg.append("rect")
      .attr("x", width + boxSpacing)
      .attr("y", (7 * lineSpaceMultiplier) + "em")
      .attr("height", "1em") 
      .attr("width", "2em")
      .style("fill", voteColors.zero)
      .style("stroke", "lavender")

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (9 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "13px") 
      .style("text-anchor", "start") 
      .style("fill", "grey")
      .text("Click a dot to visit the item.");

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (10 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "13px") 
      .style("text-anchor", "start") 
      .style("fill", "grey")
      .text("Hover over a dot to see info.");

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (13 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "12px") 
      .style("text-anchor", "start") 
      .style("fill", "grey")
      .text("Larger dots are popular.");

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (15 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "12px") 
      .style("text-anchor", "start") 
      .style("fill", "grey")
      .text("Smaller dots are unpopular,");

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (16 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "12px") 
      .style("text-anchor", "start") 
      .style("fill", "grey")
      .text("or no votes have been cast");

    svg.append("text") 
      .attr("x", width + 5)
      .attr("y", (17 * lineSpaceMultiplier) + "em")
      .attr("dy", ".85em")
      .style("font-size", "12px") 
      .style("text-anchor", "start") 
      .style("fill", "grey")
      .text("on the item.");

  </script>

</%def>
