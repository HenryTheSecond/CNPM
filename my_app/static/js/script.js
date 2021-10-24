function doanhThuNgay() {
    let date = document.getElementById("day").value
    fetch("/api/doanh-thu-ngay/" + date, {
        method: "get",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)
        let table = document.getElementById("danh_sach_ngay")
        table.innerHTML = ""
        let tong = 0
        for (i of data.danh_sach) {
            let row = table.insertRow()
            let cell = row.insertCell()
            cell.innerText = i.ten
            cell = row.insertCell()
            cell.innerText = toDateString(i.ngay_kham)
            cell = row.insertCell()
            cell.innerText = i.total
            tong += i.total
        }
        let row = table.insertRow()
        let cell = row.insertCell()
        cell = row.insertCell()
        cell = row.insertCell()
        cell.innerText = "Tổng cộng: " + tong
    })
}

function doanhThuThang() {
    let month = document.getElementById("month").value
    let year = document.getElementById("year").value
    fetch("/api/doanh-thu-thang/" + month + "-" + year, {
        method: "get",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)
        let table = document.getElementById("danh_sach_thang")
        table.innerHTML = ""
        let tong = 0
        for (i of data.doanh_thu_ngay) {
            let row = table.insertRow()
            let cell = row.insertCell()
            cell.innerText = toDateString(i.ngay_kham)
            cell = row.insertCell()
            cell.innerText = i.doanh_thu_ngay
            tong+=i.doanh_thu_ngay
        }
        let row = table.insertRow()
        let cell = row.insertCell()
        cell = row.insertCell()
        cell.innerText = "Tổng cộng: " + tong
    })
}

function toDateString(dateString){
    let date = new Date(dateString)
    return date.getDate() + "/" + (date.getMonth()+1) + "/" + date.getFullYear()
}