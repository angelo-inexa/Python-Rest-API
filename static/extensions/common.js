<<<<<<< HEAD
/**************************************************************************
 * Common js

 **************************************************************************/
jQuery(document).ready(function() {
    "use strict";


    /*  Language changer  */

    //jQuery('.language-toggle-source').on('click', function () {

    jQuery('.language-toggle-source').click(function(e){

        var language = jQuery(this).attr("data-language");

        jQuery('.code-div').removeClass('active-code');

        jQuery('.code-'+language).addClass('active-code');

        // jQuery('#' + language).addClass('active-code');
    });
    
    /* side nav categories */
    if (jQuery('.subDropdown')[0]) {
        jQuery('.subDropdown').on("click", function() {
            jQuery(this).toggleClass('plus');
            jQuery(this).toggleClass('minus');
            jQuery(this).parent().find('ul').slideToggle();
        });
    }
    jQuery.extend(jQuery.easing, {
        easeInCubic: function(x, t, b, c, d) {
            return c * (t /= d) * t * t + b;
        },
        easeOutCubic: function(x, t, b, c, d) {
            return c * ((t = t / d - 1) * t * t + 1) + b;
        },
    });
    (function(jQuery) {
        jQuery.fn.extend({
            accordion: function() {
                return this.each(function() {
                    function activate(el, effect) {
                        jQuery(el).siblings(panelSelector)[(effect || activationEffect)](((effect == "show") ? activationEffectSpeed : false), function() {
                            jQuery(el).parents().show();
                        });
                    }
                });
            }
        });
    })(jQuery);

    /*jQuery(document).ready(function() {
        slideEffectAjax();
    });*/

});

/* mobileMenu */
var isTouchDevice = ('ontouchstart' in window) || (navigator.msMaxTouchPoints > 0);
jQuery(window).load(function() {
    if (isTouchDevice) {
        jQuery('#nav a.level-top').on("click", function(e) {
            jQueryt = jQuery(this);
            jQueryparent = jQueryt.parent();
            if (jQueryparent.hasClass('parent')) {
                if (!jQueryt.hasClass('menu-ready')) {
                    jQuery('#nav a.level-top').removeClass('menu-ready');
                    jQueryt.addClass('menu-ready');
                    return false;
                } else {
                    jQueryt.removeClass('menu-ready');
                }
            }
        });
    }
});
=======
/**************************************************************************
 * Common js

 **************************************************************************/
jQuery(document).ready(function() {
    "use strict";


    /*  Language changer  */

    //jQuery('.language-toggle-source').on('click', function () {

    jQuery('.language-toggle-source').click(function(e){

        var language = jQuery(this).attr("data-language");

        jQuery('.code-div').removeClass('active-code');

        jQuery('.code-'+language).addClass('active-code');

        // jQuery('#' + language).addClass('active-code');
    });
    
    /* side nav categories */
    if (jQuery('.subDropdown')[0]) {
        jQuery('.subDropdown').on("click", function() {
            jQuery(this).toggleClass('plus');
            jQuery(this).toggleClass('minus');
            jQuery(this).parent().find('ul').slideToggle();
        });
    }
    jQuery.extend(jQuery.easing, {
        easeInCubic: function(x, t, b, c, d) {
            return c * (t /= d) * t * t + b;
        },
        easeOutCubic: function(x, t, b, c, d) {
            return c * ((t = t / d - 1) * t * t + 1) + b;
        },
    });
    (function(jQuery) {
        jQuery.fn.extend({
            accordion: function() {
                return this.each(function() {
                    function activate(el, effect) {
                        jQuery(el).siblings(panelSelector)[(effect || activationEffect)](((effect == "show") ? activationEffectSpeed : false), function() {
                            jQuery(el).parents().show();
                        });
                    }
                });
            }
        });
    })(jQuery);

    /*jQuery(document).ready(function() {
        slideEffectAjax();
    });*/

});

/* mobileMenu */
var isTouchDevice = ('ontouchstart' in window) || (navigator.msMaxTouchPoints > 0);
jQuery(window).load(function() {
    if (isTouchDevice) {
        jQuery('#nav a.level-top').on("click", function(e) {
            jQueryt = jQuery(this);
            jQueryparent = jQueryt.parent();
            if (jQueryparent.hasClass('parent')) {
                if (!jQueryt.hasClass('menu-ready')) {
                    jQuery('#nav a.level-top').removeClass('menu-ready');
                    jQueryt.addClass('menu-ready');
                    return false;
                } else {
                    jQueryt.removeClass('menu-ready');
                }
            }
        });
    }
});
>>>>>>> b123b11497a3ceb3c05fec01b1e7a892755091cd
