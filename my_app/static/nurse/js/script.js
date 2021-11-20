function tim_benh_nhan(){
    var loai_tim_kiem = document.querySelector('input[name="tim_kiem_benh_nhan"]:checked').id;
    var kw
    if(loai_tim_kiem == "tim_kiem_theo_ngay")
        kw = document.getElementById("ngay_tim_kiem").value
    else
        kw = document.getElementsByName("tim_kiem_kw")[0].value
    fetch("api/tim-benh-nhan?type=" + loai_tim_kiem + "&kw=" + kw,{
        method: "get",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res){
        console.info(res)
        return res.json()
    }).then(function(data){
        console.info(data)
        let table = document.getElementById("benh_nhan_table")
        table.innerHTML = ""
        for(i of data.danh_sach){
            let row = table.insertRow()
            let cell = row.insertCell()
            cell.innerText = i.id
            cell = row.insertCell()
            cell.innerText = i.ten
            cell = row.insertCell()
            cell.innerText = i.gioi_tinh
            cell = row.insertCell()
            cell.innerText = i.dia_chi
            cell = row.insertCell()
            cell.innerText = toDateString(i.ngay_sinh)
            cell = row.insertCell()
            cell.innerText = i.SDT
            cell = row.insertCell()
            cell.innerHTML = `<a href="/them-dskham?id=${i.id}" >Thêm</a>`
        }
    })
}

function benh_nhan_info(){
    document.getElementById("benh_nhan").style.display = "none";
    document.getElementById("ds_kham").style.display = "none"
    let table = document.getElementById("benh_nhan_info_form");
    table.style.display = "block";
}

function benh_nhan_click(){
    document.getElementById("benh_nhan_info_form").style.display = "none"
    document.getElementById("ds_kham").style.display = "none"
    let table = document.getElementById("benh_nhan")
    table.style.display = "block"
}


function ds_kham_click(){
   document.getElementById("benh_nhan").style.display = "none";
   document.getElementById("benh_nhan_info_form").style.display = "none"
   let table = document.getElementById("ds_kham");
   table.style.display = "block";
}

function xem_ds_kham(){
    let date = document.getElementById("day").value
    fetch("api/xem-dskham" + "/" + date, {
            method: "get",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(function(res){
            console.info(res)
            return res.json()
        }).then(function(data){
            console.info(data)
            let table = document.getElementById("ds_kham_table")
            table.innerHTML = ""
            let stt = 1;
            for(i of data.danh_sach){
                let row = table.insertRow()
                let cell = row.insertCell()
                cell.innerText = stt++;
                cell = row.insertCell()
                cell.innerText = i.ten
                cell = row.insertCell()
                cell.innerText = i.SDT
                cell = row.insertCell()
                cell.innerText = toDateString(i.ngay_kham)
            }
        })
}

function toDateString(dateString){
    let date = new Date(dateString)
    return date.getDate() + "/" + (date.getMonth()+1) + "/" + date.getFullYear()
}