/* This file contsins common JS */
$(document).ready(function() {
 
/* ============== Start of code ============== */
 /*== Q2 == */
 $('.hr-tab.tabs li').on('click', function(e){
    e.preventDefault();    
    var index = $(this).index();
    $('.data').attr('data-tab', index);
});

 
 /*==========Q5 popup ================ */
 
$('[data-popup-target]').click(function () {
        $('html').addClass('overlay');
        var activePopup = $(this).attr('data-popup-target');
        $(activePopup).addClass('visible');
});
$(document).keyup(function (e) {
        if (e.keyCode == 27 && $('html').hasClass('overlay')) {
            clearPopup();
        }
});

$('.popup-exit').click(function () {clearPopup(); });
$('.popup-overlay').click(function () { clearPopup();});

function clearPopup() {
  $('.popup.visible').addClass('transitioning').removeClass('visible');
  $('html').removeClass('overlay');
  setTimeout(function () {
    $('.popup').removeClass('transitioning');
    }, 200);
  }
 
/*Q. 11 youtube bar */
$({property: 0}).animate({property: 105}, {
    duration: 4000,
    step: function() {
        var _percent = Math.round(this.property);
        $('#progress').css('width',  _percent+"%");
        if(_percent == 105) {
            $("#progress").addClass("done");
        }
    },
    complete: function() {
        alert('complete');
    }
});

/*Q13 Majic line */
 var $el, leftPos, newWidth,
        $mainNav = $("#example-one");
    
    $mainNav.append("<li id='magic-line'></li>");
    var $magicLine = $("#magic-line");
    
    $magicLine
        .width($(".current_page_item").width())
        .css("left", $(".current_page_item a").position().left)
        .data("origLeft", $magicLine.position().left)
        .data("origWidth", $magicLine.width());
        
    $("#example-one li a").hover(function() {
        $el = $(this);
        leftPos = $el.position().left;
        newWidth = $el.parent().width();
        $magicLine.stop().animate({
            left: leftPos,
            width: newWidth
        });
    }, function() {
        $magicLine.stop().animate({
            left: $magicLine.data("origLeft"),
            width: $magicLine.data("origWidth")
        });    
    });
/*Q14*/

 
/* ============== End of code ============== */
})