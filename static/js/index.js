let page = 1;
let isLoading = false;
let container = $('.main-container') 

$(document).ready(function () {
    loadTableData();
    container.on('scroll', onScroll);
});

function onScroll() {
    let scrollTop = container.scrollTop();
    let scrollHeight = container[0].scrollHeight;
    let height = container.height();

    if (!isLoading) {
        if (scrollTop + height >= scrollHeight) {
            // Scrolled to bottom - load next page
            isLoading = true;
            page++;
            loadTableData();
        } else if (scrollTop === 0) {
            // Scrolled to top - load previous page
            if (page > 1) { // Avoid loading non-existing pages
                isLoading = true;
                page--;
                loadTableData();
            }
        }
    }
}

function loadTableData() {
    let queryParm = { page: page };
    console.log('Fetching data for page:', page);

    $.getJSON(`/on-scroll-data`, queryParm, function (data) {
        if (data.items && data.items.length > 0) {
            setDataTbody(data); // Replace table data
        } else {
            console.log('No data available for page:', page);
        }
        isLoading = false; // Reset loading state
    }).fail(function () {
        console.error('Error fetching data for page:', page);
        isLoading = false;
    });
}

function setDataTbody(data) {
    console.log('Replacing table data with items:', data.items);
    const rows = data.items.map((item, index) => `
        <tr>
            <td>${index + 1}</td>
            <td>${item.name}</td>
            <td>${item.age}</td>
            <td>${item.member_type}</td>
            <td>${item.description}</td>
        </tr>
    `).join('');
    $('#onScrollTable tbody').html(rows); // Replace existing data
}

// function onScroll(){
//     let scrollHeight = container[0].scrollHeight;
//     let height = container.height();

//     // console.log(container.scrollTop()+height, "her---");
//     // console.log(scrollHeight, "scheight---");

//     if(container.scrollTop()+height >= scrollHeight){
//         // console.log("unbind scroll");
//         // container.off('scroll', onScroll);
//         if (!isLoading) {
//             isLoading = true;
//             page += 1; 
//             loadTableData();
//         }
//     }
// }


// function loadTableData() {
//     queryParm ={
//         page: page
//     }
//     $.getJSON(`/on-scroll-data`, queryParm, function (data) {
//         if (data.items) {
//             setDataTbody(data);
//         } else {
//             console.log('No more data');
//             container.off('scroll', onScroll); // Unbind scroll if no more data
//         }
//     }).fail(function () {
//         console.error('Error fetching data');
//         isLoading = false;
//     }).always(function () {
//         isLoading = false; // Reset loading state
//     });
// }


// function setDataTbody(data) {
//     if (data.items && data.items.length > 0) {
//         console.log('Replacing table data with new items:', data.items);
//         const rows = data.items.map((item, index) => `
//             <tr>
//                 <td>${index + 1}</td>
//                 <td>${item.name}</td>
//                 <td>${item.age}</td>
//                 <td>${item.member_type}</td>
//                 <td>${item.description}</td>
//             </tr>
//         `).join('');
//         $('#onScrollTable tbody').html(rows); // Replace existing data
//     } else {
//         console.log('No data available to replace');
//     }
// }
