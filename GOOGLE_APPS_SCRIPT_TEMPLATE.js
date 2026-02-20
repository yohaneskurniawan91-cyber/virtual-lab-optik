function doPost(e) {
  // 1. Get the target Spreadsheet (Assuming the script is bound to the sheet, or use openById)
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("Data") || ss.insertSheet("Data");
  
  try {
    // 2. Parse the incoming JSON data
    // The Python script sends: { "experiment_data": [ ... ], "timestamp": "..." }
    var jsonData = JSON.parse(e.postData.contents);
    var dataList = jsonData.experiment_data;
    var timestamp = jsonData.timestamp;
    
    // 3. Prepare headers if sheet is empty
    if (sheet.getLastRow() === 0) {
      // Collect all keys from the first item to make headers
      var headers = ["Timestamp"];
      if (dataList.length > 0) {
        var firstItem = dataList[0];
        for (var key in firstItem) {
          headers.push(key);
        }
      }
      sheet.appendRow(headers);
    }
    
    // 4. Append Data
    var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    
    for (var i = 0; i < dataList.length; i++) {
      var item = dataList[i];
      var row = [];
      
      // Map item values to header order
      for (var h = 0; h < headers.length; h++) {
        var header = headers[h];
        if (header === "Timestamp") {
          row.push(timestamp);
        } else {
          row.push(item[header] || ""); // Empty string if key missing
        }
      }
      sheet.appendRow(row);
    }
    
    // 5. Return Success JSON
    return ContentService.createTextOutput(JSON.stringify({"status": "success", "rows": dataList.length}))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (err) {
    // Return Error JSON
    return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": err.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput("Connection OK. Use POST to send data.");
}
