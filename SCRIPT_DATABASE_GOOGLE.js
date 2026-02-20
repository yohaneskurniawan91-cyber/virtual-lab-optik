// SCRIPT GOOGLE SHEETS UNTUK VIRTUAL LAB (UPDATED WITH IDENTITY)
// Gunakan script ini untuk menangkap Data Eksperimen + Identitas Mahasiswa
// ---------------------------------------------------------------------

// KONFIGURASI ID SPREADSHEET (OPSIONAL)
// 1. Jika script ini dibuat dari menu "Extensions > Apps Script" di dalam Google Sheet, biarkan kosong ("").
// 2. Jika script ini dibuat terpisah, masukkan ID Spreadsheet di antara tanda kutip.
//    Contoh: var SPREADSHEET_ID = "1aBcD_...xyz";
var SPREADSHEET_ID = ""; 

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.tryLock(10000);
  
  try {
    // Pilih Spreadsheet berdasarkan Konfigurasi
    var doc;
    if (SPREADSHEET_ID && SPREADSHEET_ID !== "") {
      doc = SpreadsheetApp.openById(SPREADSHEET_ID);
    } else {
      doc = SpreadsheetApp.getActiveSpreadsheet();
    }
    
    // var sheet = doc.getActiveSheet(); // REMOVED: Kita akan pilih sheet dinamis
    
    // 1. Ambil Data dari Python
    var rawData = e.postData.contents;
    var jsonData = JSON.parse(rawData);
    
    // Ambil Field Utama
    var experimentData = jsonData.experiment_data; // Array data hasil lab
    var timestamp = jsonData.timestamp;
    
    // Ambil Identitas (Baru ditambahkan)
    var nama = jsonData.nama || "-";
    var nim = jsonData.nim || "-";
    var kelas = jsonData.kelas || "-";
    var module = jsonData.module || "General";
    
    // PILIH SHEET BERDASARKAN NAMA MODULE
    var sheetName = module;
    // Bersihkan nama module agar valid untuk nama sheet (opsional, tapi disarankan)
    // Ganti karakter terlarang jika ada, atau batasi panjangnya
    sheetName = sheetName.replace(/[:\/\\?*\[\]]/g, "_").substring(0, 100);
    
    var sheet = doc.getSheetByName(sheetName);
    
    // Jika sheet belum ada, BUAT BARU
    if (!sheet) {
      sheet = doc.insertSheet(sheetName);
    }
    
    // 2. Buat Header Otomatis (Jika Sheet Kosong/Baru)
    if (sheet.getLastRow() == 0) {
      // Header Default
      // Kita tidak perlu kolom "Module" lagi karena sheetnya sudah dipisah per modul
      var headers = ["Timestamp", "Nama", "NIM", "Kelas"];
      
      // Tambahkan Header dari Data Eksperimen (misal: Voltase, Arus)
      if (experimentData && experimentData.length > 0) {
        var keys = Object.keys(experimentData[0]);
        headers = headers.concat(keys);
      }
      sheet.appendRow(headers);
    }
    
    // 3. Masukkan Data Baris per Baris
    var rowsAdded = 0;
    
    // Ambil Header yang SUDAH ADA di Spreadsheet untuk memastikan urutan kolom benar
    var existingHeaders = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    
    if (experimentData) {
      for (var i = 0; i < experimentData.length; i++) {
        var item = experimentData[i];
        var row = [];
        
        // Loop setiap kolom Header yang ada di Excelnya
        for (var j = 0; j < existingHeaders.length; j++) {
           var headerName = existingHeaders[j];
           
           // Isi variasi data berdasarkan nama kolom header
           if (headerName === "Timestamp") {
             row.push(timestamp);
           } else if (headerName === "Nama") {
             row.push(nama);
           } else if (headerName === "NIM") {
             row.push(nim);
           } else if (headerName === "Kelas") {
             row.push(kelas);
           } else {
             // Jika header adalah data eksperimen (misal "Voltase")
             row.push(item[headerName] || "");
           }
        }
        sheet.appendRow(row);
        rowsAdded++;
      }
    }
    
    return ContentService.createTextOutput(JSON.stringify({
      "status": "success", 
      "rows": rowsAdded,
      "message": "Data tersimpan (Identitas + Data Lab)"
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      "status": "error", 
      "message": error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
    
  } finally {
    lock.releaseLock();
  }
}

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    "status": "success",
    "message": "Koneksi Web App Berhasil."
  })).setMimeType(ContentService.MimeType.JSON);
}