(function() {
  var curImgCount, every, fadespeed, disappearspeed, getCurImgNum, getNextImgNum, imgDirectory, numImages, showImage;

  numImages = 5;

  imgDirectory = '/images/splash/';

  curImgCount = 0;

  fadespeed = 1000;

  disappearspeed = 0

  every = function(ms, cb) {
    return setInterval(cb, ms);
  };

  getCurImgNum = function() {
    return curImgCount % numImages;
  };

  getNextImgNum = function() {
    return (curImgCount + 1) % numImages;
  };

  showImage = function() {
    var cur, curImgNum, next, nextImgNum;
    curImgNum = getCurImgNum();
    nextImgNum = getNextImgNum();
    cur = $('.textChanger' + curImgNum);
    next = $('.textChanger' + nextImgNum);
    if (numImages === 2) {
      return next.fadeIn(fadespeed, function() {
        return cur.hide();
      });
    } else {
      console.log('curImgNum: ' + curImgNum);
      /*console.log('nextImgNum: ' + nextImgNum); */
      $("div#textChanger").removeClass("hidden");
      next.fadeIn(fadespeed);
      return cur.fadeOut(disappearspeed);
    }
  };

  initialize = function() {
    var cur, curImgNum, next, nextImgNum, next1, next2, next3;
    curImgNum = getCurImgNum();
    nextImgNum = getNextImgNum();
    cur = $('.textChanger' + curImgNum);
    next = $('.textChanger' + nextImgNum);
    next1 = $('.textChanger' + (nextImgNum + 1));
    next2 = $('.textChanger' + (nextImgNum + 2));
    next3 = $('.textChanger' + (nextImgNum + 3));
    cur.hide(); 
    next.hide(); 
    /* next1.hide(); */
    next2.hide(); 
    next3.hide();
  };

  initialize();

  every(4500, function() {
    curImgCount += 1;
    return showImage();
  });

}).call(this);
