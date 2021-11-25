function bao_cao_doanh_thu_click(){
    document.getElementById("bao_cao_su_dung_thuoc").style.display = "none"
    document.getElementById("benh_nhan_da_lap_phieu").style.display = "none"
    document.getElementById("lap_phieu_hoa_don").style.display = "none"
    let table = document.getElementById("doanh_thu_info");
    table.style.display = "block";
}


function lap_hoa_don_click(){
    document.getElementById("bao_cao_su_dung_thuoc").style.display = "none"
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

    document.getElementsByName("id_kham_benh")[0].value = id
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


function bao_cao_thuoc_click(){
    document.getElementById("bao_cao_su_dung_thuoc").style.display = "block"
    document.getElementById("doanh_thu_info").style.display ="none"
    document.getElementById("lap_phieu_hoa_don").style.display = "none"
    document.getElementById("benh_nhan_da_lap_phieu").style.display = "none"
    fetch("/api/thong-ke-thuoc",{
        method: "get",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res){
        return res.json()
    }).then(function(data){

    })
}

function thanh_toan_momo(){
    /*let timestamp = new Date().valueOf()
    let requestId = "tuyen" + timestamp
    data = "accessKey=RCmyRRu3ONRNC9xm&amount=1000&extraData=&ipnUrl=voz.vn&orderId=" + requestId  +  "&orderInfo=Thanh toán qua ví MoMo&partnerCode=MOMOFIF820211121&redirectUrl=voz.vn&requestId=" + requestId  +  "&requestType=captureWallet"
    signature = CryptoJS.HmacSHA256(data, "srorZC05FI40gRaEPYCMJjFKDGjtf4BM").toString(CryptoJS.enc.Hex)
    console.log(requestId)
    console.log(signature)
    fetch("https://cors-anywhere.herokuapp.com/https://test-payment.momo.vn/v2/gateway/api/create",{
        mode: 'cors',
        method: "post",
        body: JSON.stringify({
            "partnerCode": "MOMOFIF820211121",
            "partnerName" : "Tuyen",
            "storeId" : "Tuyen",
            "requestType": "captureWallet",
            "ipnUrl": "voz.vn",
            "redirectUrl": "voz.vn",
            "orderId": requestId,
            "amount": "1000",
            "lang":  "en",
            "autoCapture": false,
            "orderInfo": "Thanh toán qua ví MoMo",
            "requestId": requestId,
            "extraData": "",
            "signature": signature
        }),
        headers: {
            "Content-Type": "application/json; charset=UTF-8",
        }
    }).then(function(res){
        console.log(res)
        return res.json()
    }).then(function(data){
        console.log(data.resultCode)
    })*/

    let timestamp = new Date().valueOf()
    let requestId = "tuyen" + timestamp
    data = "accessKey=RCmyRRu3ONRNC9xm&amount=1000&extraData=&ipnUrl=http://127.0.0.1:5000/cashier&orderId=" + requestId  +  "&orderInfo=Thanh toán qua ví MoMo&partnerCode=MOMOFIF820211121&redirectUrl=http://127.0.0.1:5000/cashier&requestId=" + requestId  +  "&requestType=captureWallet"
    signature = CryptoJS.HmacSHA256(data, "srorZC05FI40gRaEPYCMJjFKDGjtf4BM").toString(CryptoJS.enc.Hex)
    console.log(requestId)
    console.log(signature)
    fetch("/api/thanh-toan-online",{
        method: "post",
        body: JSON.stringify({
            "requestId": requestId,
            "signature": signature
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res){
        return res.json()
    }).then(function(data){
        document.getElementById("link_momo").href = data.payUrl
        document.getElementById("link_momo").innerText = data.payUrl
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