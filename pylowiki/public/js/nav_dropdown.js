(function() {
  var hidden, inside, mousein, mouseout;

  inside = false;

  hidden = true;

  mousein = function() {
    return inside = true;
  };

  mouseout = function() {
    return inside = false;
  };

  $(function() {
    var li, liHoverIn, liHoverOut, nav, navHide, navShow, toggleNav, v;
    v = $('#nav_dropdown_arrow');
    nav = $('#nav_dropdown');
    li = $('#nav_account');
    nav.hover(mousein, mouseout);
    v.hover(mousein, mouseout);
    navHide = function() {
      hidden = true;
      nav.hide();
      return li.removeClass('nav_account');
    };
    navShow = function() {
      hidden = false;
      nav.show();
      return li.addClass('nav_account');
    };
    toggleNav = function() {
      if (hidden) {
        return navShow();
      } else {
        return navHide();
      }
    };
    liHoverIn = function() {
      return li.addClass('nav_account');
    };
    liHoverOut = function() {
      if (hidden) return li.removeClass('nav_account');
    };
    navHide();
    li.hover(liHoverIn, liHoverOut);
    $('html').click(function() {
      if (!inside) return navHide();
    });
    return v.click(toggleNav);
  });

}).call(this);
