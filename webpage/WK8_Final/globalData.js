$(document).ready(function(){
    
	// Define variables that reference our script tags within the body of our page
	var topNavigation = $("#topNavigation").html();
    var footerNavigation = $("#footerNavigation").html();
    
	// Have MustacheJS render our script tags
	Mustache.parse(topNavigation);
    Mustache.parse(footerNavigation);
	
    var headerContent = {
        item:
		[
            {
                name: "Home",
                link: "./index.html",
                pageID: "index"
            },
            {
                name: "Solutions",
                link: "./solutions/index.html",
                pageID: "solutions"
            },
            {
                name: "Product Reviews",
                link: "./product_reviews/index.html",
                pageID: "reviews"
            },
            {
                name: "About Us",
                link: "./about_us/index.html",
                pageID: "about"
            }
		]
    };
    
    var currentPage = window.location.pathname;
    var currentPageElement, name;
    name = " selected-nav-item";
    
    for (var i in headerContent["item"]) {
        if (currentPage.includes(headerContent["item"][i]["pageID"]) && headerContent["item"][i]["pageID"] != "index") {
            headerContent["item"][i]["selected"]=name;
        }
    }
    
	// Define our data objects
	var topNav = Mustache.render(topNavigation, headerContent);
    var footerNav = Mustache.render(footerNavigation, headerContent);
	    
    // Place data into the HTML of our page with the html() jQuery method
    $("#render_topLinks").html(topNav);
    $("#render_footerNav").html(footerNav);
    
    // currentPageElement = document.getElementById()
    for (var i in headerContent["item"]) {
        if (currentPage.includes(headerContent["item"][i]["pageID"])) {
            var currentPageElement = document.getElementById(headerContent["item"][i]["pageID"]);
            var currentPageFooterElement = document.getElementById(headerContent["item"][i]["pageID"]+"-footer")
            if (currentPageElement && currentPageFooterElement) {
                currentPageElement.setAttribute("aria-current","page");
                currentPageFooterElement.setAttribute("aria-current","page");
            }
        }
    }


	
	// Insert current year into the Copyright text in the footer.  Note: MustacheJS is not needed to do this.
	$("#currentYear").html(new Date().getFullYear());
	
});