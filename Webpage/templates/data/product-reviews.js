$(document).ready(function(){
    
	// Define variables that reference our script tags within the body of our page
	var secondaryNavigation = $("#secondaryNavigation").html();
    var reviewPostTemplate = $("#reviewPost").html();
    
    
	// Have MustacheJS render our script tags
	Mustache.parse(secondaryNavigation);
    Mustache.parse(reviewPostTemplate);
    
	
    var secondaryHeaderContent = {
        item:
		[
            {
                name: "Show All",
                link: "./index.html",
                pageID: "index",
                icon: "fas fa-th-list"
            },
            {
                name: "Electrical",
                link: "./electrical.html",
                pageID: "electrical",
                icon: "fas fa-plug"
            },
            {
                name: "HVAC",
                link: "./hvac.html",
                pageID: "hvac",
                icon: "fas fa-snowflake"
            },
            {
                name: "Plumbing",
                link: "./plumbing.html",
                pageID: "plumbing",
                icon: "fas fa-faucet",
            },
            {
                name: "Solar",
                link: "./solar.html",
                pageID: "solar",
                icon: "fas fa-solar-panel"
            },
            {
                name: "Networking",
                link: "./networking.html",
                pageID: "networking",
                icon: "fas fa-wifi",
            },
            {
                name: "Security",
                link: "./security.html",
                pageID: "security",
                icon: "fas fa-key",
            },
            {
                name: "Smart Home",
                link: "./smart-home.html",
                pageID: "smart-home",
                icon: "fas fa-house-user",
            }
		]
    };
    
    var currentPage = window.location.pathname;
    var currentPageElement, name;
    name = " selected-secondary-nav-item";
    
    for (var i in secondaryHeaderContent["item"]) {
        if (currentPage.includes(secondaryHeaderContent["item"][i]["pageID"])) {
            secondaryHeaderContent["item"][i]["selected"]=name;
        }
    }
    
	// Define our data objects
	var secondNav = Mustache.render(secondaryNavigation, secondaryHeaderContent);
    // var footerNav = Mustache.render(footerNavigation, headerContent);
	    
    // Place data into the HTML of our page with the html() jQuery method
    $("#render_secondNavLinks").html(secondNav);


    
    var reviewContents = {
        allItems:
        [
            {
                image: "https://m.media-amazon.com/images/I/71b86zpoeuL._AC_UL320_.jpg",
                altText: "Faucet",
                title: "Shiny Faucet",
                text: "This is the product review for the thing. Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "16"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/100127/1001276940.jpg?size=xl",
                altText: "Product Image 2",
                title: "Solar Panel 1",
                text: "This is the product review for the thing. Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "15"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/100313/1003131348.jpg?size=xl",
                altText: "Product Image 3",
                title: "Solar Panel 2",
                text: "This is the product review for the thing. Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "14"
            },
            {
                image: "https://www.casetawireless.com/style%20library/caseta/images/CasetaProducts/In-wall-dimmer-big.png",
                altText: "Caseta Smart Switch",
                title: "Caseta Smart Switch",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "13"
            },
            {
                image: "https://m.media-amazon.com/images/I/61EgKv96u2L._AC_UL320_.jpg",
                altText: "MyQ Smart Garage Door Opener",
                title: "MyQ Smart Garage Door Opener",
                text: "This is the product review for the thing. Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "12"
            },
            {
                image: "https://m.media-amazon.com/images/I/61eNVygMPRL._AC_UY218_.jpg",
                altText: "Window Air Conditioner",
                title: "Window A/C",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "11"
            },
            {
                image: "https://m.media-amazon.com/images/I/61GPF6q0chL._AC_UL320_.jpg",
                altText: "Space Heater",
                title: "Space Heater",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "10"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/783164/783164302431.jpg?size=xl",
                altText: "Circuit Breaker Panel",
                title: "Circuit Breaker Panel",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "9"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/054732/054732806676.jpg?size=xl",
                altText: "Medium Duty Red Extension Cord",
                title: "Medium Duty Extension Cord",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "8"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/100301/1003011300.jpg?size=xl",
                altText: "Cat 6 Cable - 1000ft",
                title: "Bulk Cat 6 Cable",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "7"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/100313/1003138782.jpg?size=xl",
                altText: "Cat 6 cable coil",
                title: "Cat 6 Keystone Wall Termination",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "6"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/100255/1002552216.jpg?size=xl",
                altText: "5-port Ethernet Switch",
                title: "5-Port 10/100 Gigabit Ethernet Switch",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "5"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/193108/193108140973.jpg?size=xl",
                altText: "Security Camera",
                title: "Security Camera",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "4"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/043156/043156171163.jpg?size=pdhi",
                altText: "Deadbolt",
                title: "Deadbolt",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "3"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/845473/845473041590.jpg?size=pdhi",
                altText: "Motion Sensor",
                title: "Motion Sensor",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "2"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/019800/019800001094.jpg?size=xl",
                altText: "Drain Cleaner",
                title: "Drain Cleaner",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "1"
            }
        ],
        electrical:
        [
            {
                image: "https://mobileimages.lowes.com/product/converted/783164/783164302431.jpg?size=xl",
                altText: "Circuit Breaker Panel",
                title: "Circuit Breaker Panel",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "9"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/845473/845473041590.jpg?size=pdhi",
                altText: "Motion Sensor",
                title: "Motion Sensor",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "2"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/054732/054732806676.jpg?size=xl",
                altText: "Medium Duty Red Extension Cord",
                title: "Medium Duty Extension Cord",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "8"
            }
        ],
        hvac:
        [
            {
                image: "https://m.media-amazon.com/images/I/61eNVygMPRL._AC_UY218_.jpg",
                altText: "Window Air Conditioner",
                title: "Window A/C",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "11"
            },
            {
                image: "https://m.media-amazon.com/images/I/61GPF6q0chL._AC_UL320_.jpg",
                altText: "Space Heater",
                title: "Space Heater",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "10"
            }
        ],
        plumbing:
        [
            {
                image: "https://m.media-amazon.com/images/I/71b86zpoeuL._AC_UL320_.jpg",
                altText: "Faucet",
                title: "Shiny Faucet",
                text: "This is the product review for the thing. Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "16"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/019800/019800001094.jpg?size=xl",
                altText: "Drain Cleaner",
                title: "Drain Cleaner",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "1"
            }
        ],
        solar:
        [
            {
                image: "https://mobileimages.lowes.com/product/converted/100127/1001276940.jpg?size=xl",
                altText: "Product Image 2",
                title: "Solar Panel 1",
                text: "This is the product review for the thing. Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "123"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/100313/1003131348.jpg?size=xl",
                altText: "Product Image 3",
                title: "Solar Panel 2",
                text: "This is the product review for the thing. Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "123"
            }
        ],
        networking:
        [
            {
                image: "https://mobileimages.lowes.com/product/converted/100301/1003011300.jpg?size=xl",
                altText: "Cat 6 Cable - 1000ft",
                title: "Bulk Cat 6 Cable",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "7"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/100313/1003138782.jpg?size=xl",
                altText: "Cat 6 cable coil",
                title: "Cat 6 Keystone Wall Termination",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "6"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/100255/1002552216.jpg?size=xl",
                altText: "5-port Ethernet Switch",
                title: "5-Port 10/100 Gigabit Ethernet Switch",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "5"
            }
        ],
        security:
        [
            {
                image: "https://mobileimages.lowes.com/product/converted/193108/193108140973.jpg?size=xl",
                altText: "Security Camera",
                title: "Security Camera",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "4"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/845473/845473041590.jpg?size=pdhi",
                altText: "Deadbolt",
                title: "Deadbolt",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "3"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/845473/845473041590.jpg?size=mthb",
                altText: "Motion Sensor",
                title: "Motion Sensor",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "2"
            }
        ],
        smart_home:
        [
            {
                image: "https://www.casetawireless.com/style%20library/caseta/images/CasetaProducts/In-wall-dimmer-big.png",
                altText: "Caseta Smart Switch",
                title: "Caseta Smart Switch",
                text: "This is the product review for the thing. Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "13"
            },
            {
                image: "https://mobileimages.lowes.com/product/converted/845473/845473041590.jpg?size=pdhi",
                altText: "Motion Sensor",
                title: "Motion Sensor",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "2"
            },
            {
                image: "https://m.media-amazon.com/images/I/61EgKv96u2L._AC_UL320_.jpg",
                altText: "MyQ Smart Garage Door Opener",
                title: "MyQ Smart Garage Door Opener",
                text: "This is the product review for the thing. Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                reviewID: "12"
            }
        ]
    };
    var prodReviews = Mustache.render(reviewPostTemplate, reviewContents);
    $("#render_reviews").html(prodReviews);

	
});