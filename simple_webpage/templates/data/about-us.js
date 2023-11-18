$(document).ready(function(){
    
	// Define variables that reference our script tags within the body of our page
	var secondaryNavigation = $("#secondaryNavigation").html();
    // var footerNavigation = $("#footerNavigation").html();
    
    
	// Have MustacheJS render our script tags
	Mustache.parse(secondaryNavigation);
    
	
    var secondaryHeaderContent = {
        item:
		[
            {
                name: "Contact Us",
                link: "./contact_us.html",
                pageID: "contact_us",
                icon: "fa-phone"
            },
            {
                name: "Our History",
                link: "./our_history.html",
                pageID: "history",
                icon: "fa-history"
            },
            {
                name: "Our Team",
                link: "./our_team.html",
                pageID: "team",
                icon: "fa-users",
                
            },
            {
                name: "Careers",
                link: "./careers.html",
                pageID: "careers",
                icon: "fa-briefcase"
            }
		]
    };
    
    var currentPage = window.location.pathname;
    var currentPageElement, name;
    name = " selected-secondary-nav-item";
    
    for (var i in secondaryHeaderContent["item"]) {
        if (currentPage.includes(secondaryHeaderContent["item"][i]["pageID"]) && secondaryHeaderContent["item"][i]["pageID"] != "index") {
            secondaryHeaderContent["item"][i]["selected"]=name;
        }
    }
    
	// Define our data objects
	var secondNav = Mustache.render(secondaryNavigation, secondaryHeaderContent);
    // var footerNav = Mustache.render(footerNavigation, headerContent);
	    
    // Place data into the HTML of our page with the html() jQuery method
    $("#render_secondNavLinks").html(secondNav);
   
    // currentPageElement = document.getElementById()
    for (var i in secondaryHeaderContent["item"]) {
        if (currentPage.includes(secondaryHeaderContent["item"][i]["pageID"])) {
            var currentPageElement = document.getElementById(secondaryHeaderContent["item"][i]["pageID"]);
            if (currentPageElement) {
                currentPageElement.setAttribute("aria-current","sub-page");
            }
        }
    }
	
});