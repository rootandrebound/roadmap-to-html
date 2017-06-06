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

  // $('body > #site-navigation, body > main').css({
  // 		'transition': 'left 0.5s ease-in-out'
  // });

  function catchAllClicksAndCloseSideMenu(event){
    event.stopImmediatePropagation();
    closeSideMenu();
  }

  function openSideMenu(){
    body.addClass('menu-active');
    if (isOnSmallScreen){
      // catch any clicks on the main node and use it to trigger collapse
      mainNode.on('click', catchAllClicksAndCloseSideMenu);
    }
  }

  function closeSideMenu(){
    if (isOnSmallScreen){
      mainNode.off('click', catchAllClicksAndCloseSideMenu);
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

  //if screen is larger than 900px:
  	// add class
  //if open page the menu is already open
  //if screen is smaller close menu automatically

});