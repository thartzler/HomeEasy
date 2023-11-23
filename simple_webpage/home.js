$(document).ready(function(){
    
	// Define variables that reference our script tags within the body of our page
    var reviewCardTemplate = $("#reviewCard").html();
    var reviewPostPreview = $("#reviewPostPreview").html();
    
    
    
	// Have MustacheJS render our script tags
    Mustache.parse(reviewCardTemplate);
	Mustache.parse(reviewPostPreview);
    

    

	var reviewCards = {
        review:
        [
            {
                title: "What Wonderful Service",
                star_1: "checked",
                star_2: "checked",
                star_3: "checked",
                star_4: "checked",
                star_5: "checked",
                text: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Velit consectetur expedita vel hic odit, ratione ipsa nam labore asperiores inventore harum aliquam alias eligendi. Aut, id dolores. Vitae, doloremque fugiat!",
                author: "me"
            },
            {
                title: "What A Great Resource",
                star_1: "checked",
                star_2: "checked",
                star_3: "checked",
                star_4: "checked",
                star_5: "checked",
                text: "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Inventore, delectus numquam minima rerum beatae esse dolorum consectetur magni fuga dignissimos adipisci eius? Harum odit quisquam, ducimus fugiat excepturi ratione quas.",
                author: "me"
            },
            {
                title: "Review Number",
                star_1: "checked",
                star_2: "checked",
                star_3: "checked",
                star_4: "checked",
                star_5: "",
                text: "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Deleniti saepe, atque facere est eius illum molestias adipisci beatae commodi quaerat? Nisi fuga eum minus eveniet doloribus nihil. Recusandae, consequuntur minus?",
                author: "me"
            }
        ]
    };

    reviewCards["review"][0]["isActive"]="active"

    var companyReviews = Mustache.render(reviewCardTemplate, reviewCards);

    $("#rendered_review_carousel").html(companyReviews);



	var reviewPreviews = {
        item:
        [
            {
                image: "https://www.casetawireless.com/style%20library/caseta/images/CasetaProducts/In-wall-dimmer-big.png",
                altText: "Product Image 1",
                title: "Product Review 1",
                text: "This is the product review for the thing. Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                link: "#"
            },
            {
                image: "https://www.casetawireless.com/style%20library/caseta/images/CasetaProducts/In-wall-dimmer-big.png",
                altText: "Product Image 2",
                title: "Product Review 2",
                text: "This is the product review for the thing. Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                link: "#"
            },
            {
                image: "https://www.casetawireless.com/style%20library/caseta/images/CasetaProducts/In-wall-dimmer-big.png",
                altText: "Product Image 3",
                title: "Product Review 3",
                text: "This is the product review for the thing. Lorem ipsum dolor, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                link: "#"
            },
            {
                image: "https://www.casetawireless.com/style%20library/caseta/images/CasetaProducts/In-wall-dimmer-big.png",
                altText: "Product Image 4",
                title: "Product Review 4",
                text: "This is the product review for the thing. Lorem ipsum dolor55, sit amet consectetur adipisicing elit. Laudantium, placeat nisi nemo pariatur eius quam officia asperiores distinctio! Aliquam debitis reprehenderit omnis cumque eum placeat illum corporis consequuntur, aliquid natus.",
                link: "#"
            }
        ]
    };
    var prodReviews = Mustache.render(reviewPostPreview, reviewPreviews);
    $("#render_reviews").html(prodReviews);


	
});