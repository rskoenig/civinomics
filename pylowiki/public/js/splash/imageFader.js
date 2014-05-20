(function() {
  var curImgCount, every, fadespeed, getCurImgNum, getNextImgNum, imgDirectory, numImages, showImage;

  numImages = 5;

  imgDirectory = '/images/splash/';

  curImgCount = 0;

  fadespeed = 1000;

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
    cur = $('.imageChanger' + curImgNum);
    next = $('.imageChanger' + nextImgNum);
    if (numImages === 2) {
      return next.fadeIn(fadespeed, function() {
        return cur.hide();
      });
    } else {
      console.log('curImgNum: ' + curImgNum);
      console.log('nextImgNum: ' + nextImgNum);
      next.fadeIn(fadespeed);
      return cur.fadeOut(fadespeed);
    }
  };

  every(4500, function() {
    curImgCount += 1;
    return showImage();
  });

}).call(this);
