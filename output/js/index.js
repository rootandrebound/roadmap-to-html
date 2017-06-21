var ALGOLIA_APP_ID = "ER4XGAZU3H";
var ALGOLIA_PUBLIC_KEY = "ad6b289aa74181fef926dc6133bfece7";

function initializeSearch() {
  var searchInput = $('#search-input input[type="text"]');
  console.log('searchInput', searchInput);
  var client = algoliasearch(ALGOLIA_APP_ID, ALGOLIA_PUBLIC_KEY);
  var index = client.initIndex('test_ROADMAP');
  console.log("initialized search", client)
  searchInput.autocomplete(
    { hint: false },
    [
      {
        source: $.fn.autocomplete.sources.hits(index, { hitsPerPage: 10 }),
        displayKey: 'title',
        templates: {
          suggestion: function(suggestion) {
            console.log('suggestion:', suggestion);
            return suggestion._highlightResult.title.value+"<super>2<super>";
          }
        }
      }
    ]
  ).on('autocomplete:selected', function(event, suggestion, dataset) {
    console.log("this is suggestion:", suggestion, "this is dataset:", dataset);
  });
}

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

  initializeSearch();
});