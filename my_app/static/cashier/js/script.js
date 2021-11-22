function bao_cao_doanh_thu_click(){
    document.getElementById("benh_nhan_da_lap_phieu").style.display = "none"
    document.getElementById("lap_phieu_hoa_don").style.display = "none"
    let table = document.getElementById("doanh_thu_info");
    table.style.display = "block";
}


function lap_hoa_don_click(){
    document.getElementById("doanh_thu_info").style.display = "none"
    document.getElementById("lap_phieu_hoa_don").style.display = "none"
    let table = document.getElementById("benh_nhan_da_lap_phieu");
    table.style.display = "block";
    fetch("api/xem-ds-phieu", {
            method: "get",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(function(res){
            console.info(res)
            return res.json()
        }).then(function(data){
            console.info(data)
            let table = document.getElementById("benh_nhan_da_lap_phieu_table")
            table.innerHTML = ""
            for(i of data.danh_sach){
                let row = table.insertRow()
                let cell = row.insertCell()
                cell.innerText = i.kham_benh_id
                cell = row.insertCell()
                cell.innerText = i.ten_benh_nhan
                cell = row.insertCell()
                cell.innerText = i.trieu_chung
                cell = row.insertCell()
                cell.innerText = i.ten_benh
                cell = row.insertCell()
                cell.innerText = toDateString(i.ngay_kham)
                cell = row.insertCell()
                cell.innerHTML = `<a href="javascript:;"  onclick="chon_click(${i.kham_benh_id})" >Chọn</a>`
            }
        })
}

function chon_click(id){
    document.getElementById("benh_nhan_da_lap_phieu").style.display = "none"
    document.getElementById("doanh_thu_info").style.display = "none"
    let table = document.getElementById("lap_phieu_hoa_don");
    let id_kham_benh = document.getElementById("id_kham_benh");
    id_kham_benh.innerText = id;
    table.style.display = "block";
}


function them_thuoc_click(thuoc){
    let clone = document.getElementsByName("don_thuoc")[0].cloneNode( true );
    document.getElementById("don_thuoc").appendChild(clone)
    console.log(clone)
}

async function create_bill_id(id_kham_benh) {
    await fetch("/api/create-bill-id" + "/" + id_kham_benh, {
        method: 'get',
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)
    })
}

async function create_bill_total(id_kham_benh) {
    await fetch("/api/create-bill-total" + "/" + id_kham_benh, {
        method: 'get',
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)
        alert("thoanh toán thành công")
    })
}


async function create_bill(id_kham_benh, id_thuoc, gia, so_luong) {
    await fetch("/api/create-bill", {
        method: 'post',
        body: JSON.stringify({
            "id_kham_benh": id_kham_benh,
            "id_thuoc": id_thuoc,
            "gia": gia,
            "so_luong": so_luong
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)
    })
}


async function lap_hoa_don(){
    var chi_tiet_hoa_don = document.getElementsByClassName("hoa_don");
    let id =  document.getElementById("id_kham_benh").innerText;
    await create_bill_id(id)
    var i
    for (i = 0; i < chi_tiet_hoa_don.length; i+=3) {
        await updateThuoc(chi_tiet_hoa_don[i].value, chi_tiet_hoa_don[i+2].value)
        await create_bill(id, chi_tiet_hoa_don[i].value, chi_tiet_hoa_don[i+1].value, chi_tiet_hoa_don[i+2].value)
    }

    await create_bill_total(id)
}


function toDateString(dateString){
    let date = new Date(dateString)
    return date.getDate() + "/" + (date.getMonth()+1) + "/" + date.getFullYear()
}

async function updateThuoc(thuoc_id, so_luong) {
    await fetch("/api/update-soluong-thuoc/", {
        method: "put",
        body: JSON.stringify({
            "thuoc_id": parseInt(thuoc_id),
            "so_luong": parseInt(so_luong)
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        return res.json()
    }).then(function(data){
        if (data.error_code == 500){
            alert("Không đủ thuốc")
        }
    })
}



//async function checkThuoc(thuoc_id, so_luong) {
//    await fetch("/api/check-soluong-thuoc/" + thuoc_id + "-" + so_luong, {
//        method: "get",
//        headers: {
//            "Content-Type": "application/json"
//        }
//    }).then(function(res) {
//        return res.json()
//    }).then(function(data){
//        console.log(data)
//    })
//}