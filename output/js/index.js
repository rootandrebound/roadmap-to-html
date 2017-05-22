$(function() {
  // Runs as soon as the page loads
  var isOnSmallScreen = $('body').width() < 900;
  var doc = $(document);
  var body = $('body');

  var mainNode = $('main');

  function menuIsOpen(){
    return body.hasClass('menu-active');
  }

  if (isOnSmallScreen === false && menuIsOpen() === false){
    // if we are on a big screen, open the menu by default
    openSideMenu();
  }

  function openSideMenu(){
    body.addClass('menu-active');
    if (isOnSmallScreen){
      // catch any clicks on the main node and use it to trigger collapse
      mainNode.on('click', function(event){
        event.stopImmediatePropagation();
        closeSideMenu();
      });

    }
  }

  function closeSideMenu(){
    if (isOnSmallScreen){
      mainNode.off('click');
    }
    body.removeClass('menu-active')
  }



  doc.on('click', '#js-toggle-menu', function(){
    if (menuIsOpen()){
      closeSideMenu();
    } else {
      openSideMenu();
    }
  });


});