function px(value){
  // coerce to string
  value = value + '';
  if( value.indexOf('px') === -1) {
    value += 'px';
  }
  return value;
}

$(function() {

  /*
  open state:
    #site-navigation left = 0
    main left = width
  closed state:
    #site-navigation left = -width
    main left = 0
  */

  // Runs as soon as the page loads
  var isOnSmallScreen = $('body').width() < 900;
  var doc = $(document);
  var body = $('body');

  var mainNode = $('main');
  var sideNav = $('#site-navigation');
  var sideNavWidth = px(sideNav.css('width'));

  function menuIsOpen(){
    return (
      sideNav.css('left') === px(0)
    ) && (
      mainNode.css('left') === px(sideNavWidth)
    );
  }

  if (isOnSmallScreen === false && menuIsOpen() === false){
    // if we are on a big screen, open the menu by default
    openSideMenu();
  }

  function catchAllClicksAndCloseSideMenu(event){
    event.stopImmediatePropagation();
    closeSideMenu();
  }

  function openSideMenu(){
    sideNav.animate({'left': px(0)});
    mainNode.animate({'left': px(sideNavWidth)});
    if (isOnSmallScreen){
      // catch any clicks on the main node and use it to trigger collapse
      mainNode.on('click', catchAllClicksAndCloseSideMenu);
    }
  }

  function closeSideMenu(){
    if (isOnSmallScreen){
      mainNode.off('click', catchAllClicksAndCloseSideMenu);
    }
    sideNav.animate({'left': '-' + px(sideNavWidth)});
    mainNode.animate({'left': px(0)});
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