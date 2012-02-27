/*
 * Script from NETTUTS.com [modified by Mario Jimenez] V.3 (ENHANCED, WITH DATABASE & ADD WIDGETS FEATURE!!!)
 * @requires jQuery($), jQuery UI & sortable/draggable UI modules
 */

var iNettuts = {
    
    jQuery : $,
    
    settings : {
        columns : '.column',
        widgetSelector: '.widget',
        handleSelector: '.widget-head',
        contentSelector: '.widget-content',
        postPath: '/slideshow/edit',
        
        saveToDB: true,
        
        widgetDefault : {
            movable: true,
            removable: false,
            collapsible: false,
            editable: true,
            colorClasses: ['color-yellow', 'color-red', 'color-blue', 'color-white', 'color-orange', 'color-green'],
            content: "<div align='center'><img src='/images/load.gif' border='0' /></div>"
        },
        widgetIndividual : {}
    },

    init : function () {
        this.attachStylesheet('/styles/inettuts.js.css');
        //$('body').css({background:'#000'});
        //$(this.settings.columns).css({visibility:'visible'});
        //this.sortWidgets();
        this.addWidgetControls();
        this.makeSortable();
    },
    
    initWidget : function (opt) {
      if (!opt.content) opt.content=iNettuts.settings.widgetDefault.content;
      return '<li id="'+opt.id+'" class="new widget '+opt.color+'"><div class="widget-head"><h3>'+opt.title+'</h3></div><div class="widget-content">'+opt.content+'</div></li>';
    },
    
    
    loadWidget : function(id) {
        /*
      $.post("widgets_rpc.php", {"id":id},
      function(data){
        $("#"+id+" "+iNettuts.settings.contentSelector).html(data);
      });
      */
    },
    
    addWidget : function (where, opt) {
      $("li").removeClass("new");
      var selectorOld = iNettuts.settings.widgetSelector;
      iNettuts.settings.widgetSelector = '.new';
      $(where).append(iNettuts.initWidget(opt));
      iNettuts.addWidgetControls();
      iNettuts.settings.widgetSelector = selectorOld;
      iNettuts.makeSortable();
      iNettuts.savePreferences();
      iNettuts.loadWidget(opt.id);
    },
    
    
    getWidgetSettings : function (id) {
        var $ = this.jQuery,
            settings = this.settings;
        return (id&&settings.widgetIndividual[id]) ? $.extend({},settings.widgetDefault,settings.widgetIndividual[id]) : settings.widgetDefault;
    },
    
    addWidgetControls : function () {
        var iNettuts = this,
            $ = this.jQuery,
            settings = this.settings;
            
        $(settings.widgetSelector, $(settings.columns)).each(function () {
            var thisWidgetSettings = iNettuts.getWidgetSettings(this.id);
            if (thisWidgetSettings.removable) {
                $('<a href="#" class="remove">CLOSE</a>').mousedown(function (e) {
                    /* STOP event bubbling */
                    e.stopPropagation();    
                }).click(function () {
                    if(confirm('This widget will be removed, ok?')) {
                        $(this).parents(settings.widgetSelector).animate({
                            opacity: 0    
                        },function () {
                            $(this).wrap('<div/>').parent().slideUp(function () {
                                $(this).remove();
                                iNettuts.savePreferences();
                            });
                        });
                    }
                    return false;
                }).appendTo($(settings.handleSelector, this));
            }
            
            if (thisWidgetSettings.editable) {
                $('<a href="#" class="edit">EDIT</a>').mousedown(function (e) {
                    /* STOP event bubbling */
                    e.stopPropagation();    
                }).toggle(function () {
                    $(this).css({backgroundPosition: '-66px 0', width: '55px'})
                        .parents(settings.widgetSelector)
                            .find('.edit-box').show().find('input').focus();
                    return false;
                },function () {
                    $(this).css({backgroundPosition: '', width: '24px'})
                        .parents(settings.widgetSelector)
                            .find('.edit-box').hide();
                    iNettuts.savePreferences();
                    return false;
                }).appendTo($(settings.handleSelector,this));
                $('<div class="edit-box" style="display:none;"/>')
                    .append('<ul><li class="item"><label>Change the title?</label><input value="' + $('h3',this).text() + '" id = "title"/></li>')
                    .append('<ul><li class="item"><label>Change the caption?</label><input value="' + $('p',this).text() + '" id = "caption"/></li>')
                    .append('</ul>')
                    .insertAfter($(settings.handleSelector,this));
            }
            
            if (thisWidgetSettings.collapsible) {
                $('<a href="#" class="collapse">COLLAPSE</a>').mousedown(function (e) {
                    /* STOP event bubbling */
                    e.stopPropagation();    
                }).click(function(){
                    $(this).parents(settings.widgetSelector).toggleClass('collapsed');
                    /* Save prefs to cookie: */
                    //iNettuts.savePreferences();
                    return false;    
                }).prependTo($(settings.handleSelector,this));
            }
        });
        
        $('.edit-box').each(function () {
            $('input#title',this).keyup(function () {
                $(this).parents(settings.widgetSelector).find('h3').text( $(this).val().length>20 ? $(this).val().substr(0,20)+'...' : $(this).val() );
                //iNettuts.savePreferences();
            });
            $('input#caption',this).keyup(function () {
                $(this).parents(settings.widgetSelector).find('p').text( $(this).val() );
                //iNettuts.savePreferences();
            });
            $('ul.colors li',this).click(function () {
                
                var colorStylePattern = /\bcolor-[\w]{1,}\b/,
                    thisWidgetColorClass = $(this).parents(settings.widgetSelector).attr('class').match(colorStylePattern)
                if (thisWidgetColorClass) {
                    $(this).parents(settings.widgetSelector)
                        .removeClass(thisWidgetColorClass[0])
                        .addClass($(this).attr('class').match(colorStylePattern)[0]);
                    /* Save prefs to cookie: */
                    iNettuts.savePreferences();
                }
                return false;
                
            });
        });
        
    },
    
    attachStylesheet : function (href) {
        var $ = this.jQuery;
        return $('<link href="' + href + '" rel="stylesheet" type="text/css" />').appendTo('head');
    },
    
    makeSortable : function () {
        var iNettuts = this,
            $ = this.jQuery,
            settings = this.settings,
            $sortableItems = (function () {
                var notSortable = '';
                $(settings.widgetSelector,$(settings.columns)).each(function (i) {
                    if (!iNettuts.getWidgetSettings(this.id).movable) {
                        if(!this.id) {
                            this.id = 'widget-no-id-' + i;
                        }
                        notSortable += '#' + this.id + ',';
                    }
                });
                if (notSortable=='')
                  return $("> li", settings.columns);
                else
                  return $('> li:not(' + notSortable + ')', settings.columns);
            })();
        
        $sortableItems.find(settings.handleSelector).css({
            cursor: 'move'
        }).mousedown(function (e) {
            $sortableItems.css({width:''});
            $(this).parent().css({
                width: $(this).parent().width() + 'px'
            });
        }).mouseup(function () {
            if(!$(this).parent().hasClass('dragging')) {
                $(this).parent().css({width:''});
                iNettuts.savePreferences();
            } else {
                $(settings.columns).sortable('disable');
                iNettuts.savePreferences();
            }
        });

        $(settings.columns).sortable('destroy');
        $(settings.columns).sortable({
            items: $sortableItems,
            connectWith: $(settings.columns),
            handle: settings.handleSelector,
            placeholder: 'widget-placeholder',
            forcePlaceholderSize: true,
            revert: 300,
            delay: 100,
            opacity: 0.8,
            containment: 'document',
            start: function (e,ui) {
                $(ui.helper).addClass('dragging');
            },
            stop: function (e,ui) {
                $(ui.item).css({width:''}).removeClass('dragging');
                $(settings.columns).sortable('enable');
                iNettuts.savePreferences();
            }
        });
    },
    
    savePreferences : function () {
        var iNettuts = this,
            $ = this.jQuery,
            settings = this.settings,
            cookieString = '';
            
        if(!settings.saveToDB) {return;}
        
        /* Assemble the cookie string */
        $(settings.columns).each(function(i){
            cookieString += (i===0) ? '' : '|';
            $(settings.widgetSelector,this).each(function(i){
                cookieString += (i===0) ? '' : ';|;';
                /* ID of widget: */
                cookieString += $(this).attr('id') + '||';
                /* Color of widget (color classes) */
                //cookieString += $(this).attr('class').match(/\bcolor-[\w]{1,}\b/) + ',';
                /* Title of widget (replaced used characters) */
                cookieString += $('h3:eq(0)',this).text().replace(/\|/g,'[-PIPE-]').replace(/,/g,'[-COMMA-]') + '||';
                cookieString += $('p:eq(0)',this).text();
                /* Collapsed/not collapsed widget? : */
                //cookieString += $(settings.contentSelector,this).css('display') === 'none' ? 'collapsed' : 'not-collapsed';
            });
        });
        
        /* AJAX call to store string on database */
        //$.post(settings.postPath,"value="+cookieString);
        $.post(settings.postPath, {string : cookieString}, 'json')
    },
    
    sortWidgets : function () {
        var iNettuts = this,
            $ = this.jQuery,
            settings = this.settings;
        
        if(!settings.saveToDB) {
            $('body').css({background:'#000'});
            $(settings.columns).css({visibility:'visible'});
            return;
        }
        
        $.post ( settings.postPath, "",
            function(data){
        
              var cookie=data;
              
              if (cookie=="") {
                  $('body').css({background:'#000'});
                  $(settings.columns).css({visibility:'visible'});
                  iNettuts.addWidgetControls();
                  iNettuts.makeSortable();
                  return;
              }
               
              /* For each column */
              $(settings.columns).each(function(i){
                  
                  var thisColumn = $(this),
                      widgetData = cookie.split('|')[i].split(';');
                      
                  $(widgetData).each(function(){
                      if(!this.length) {return;}
                      
                      var thisWidgetData = this.split(','),
                          opt={
                            id: thisWidgetData[0],
                            color: thisWidgetData[1],
                            title: thisWidgetData[2].replace(/\[-PIPE-\]/g,'|').replace(/\[-COMMA-\]/g,','),
                            content: settings.widgetDefault.content
                          };
                      $(thisColumn).append(iNettuts.initWidget(opt));
                      if (thisWidgetData[3]==='collapsed') $('#'+thisWidgetData[0]).addClass('collapsed');
                      iNettuts.loadWidget(thisWidgetData[0]);
                  });
              });
              
              /* All done, remove loading gif and show columns: */
              $('body').css({background:'#000'});
              $(settings.columns).css({visibility:'visible'});
              
              iNettuts.addWidgetControls();
              iNettuts.makeSortable();
              
            });
    }
};

iNettuts.init();