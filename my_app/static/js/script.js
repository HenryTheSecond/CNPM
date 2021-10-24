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
            cell.innerText = i.ngay_kham
            cell = row.insertCell()
            cell.innerText = i.total
            tong += i.total
        }
        let tong_span = document.getElementById("tong_tien")
        tong_span.innerText = tong
    })
}