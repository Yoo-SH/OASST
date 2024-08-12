/**
 * 이진채라는 단어로 특정 셀의 값을 변경하는 코드 예시
 */
function updateGColumnIfFContains() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Sheet1"); // 시트 지정
  var startRow = 12000; // 수정할 row 범위 지정
  var endRow = 15000;
  var targetWord = "이진채"; // 특정 단어를 기준으로 조건 검사

  for (var row = startRow; row <= endRow; row++) {
    var currentRowValues = sheet
      .getRange(row, 1, 1, sheet.getLastColumn())
      .getValues()[0]; // 현재 행의 모든 값 가져오기

    // F열 값 가져오기
    var fColumnValue = currentRowValues[5]; // F열은 인덱스 5 (0부터 시작)

    // F열에 "이진채"라는 단어가 독립적으로 존재하는 경우에만 처리
    if (
      typeof fColumnValue === "string" &&
      fColumnValue.indexOf(targetWord) !== -1
    ) {
      // G열의 값을 0으로 설정
      sheet.getRange(row, 7).setValue("FALSE"); // G열은 7번째 열
    }
  }
}

/**
 * 답변이라는 단어로 자문 자답을 분리한 코드 예시
 * 네이버 카페의 경우, prompt가 자문자답을 하고 끝나는 경우가 종종 있음.
 * 질문을 prompt로 남기고, 답변을 assistant로 행을 추가하여 내리는 코드를 추가.
 * 자문자답의 경우, 특정 단어로 분리되는 경우가 대부분 (ex  ‘답변’, ‘A’)
 */
function copyAndMoveResponse() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Sheet1"); //시트 지정
  var startRow = 5568; //수정할 row 범위 지정
  var endRow = 6000;
  var separation_word = "답변"; //특정 단어를 기준으로 자문자답을 분리시켜 행을 추가하고 트리구조를 유지

  for (var row = startRow; row <= endRow; row++) {
    var currentRowValues = sheet
      .getRange(row, 1, 1, sheet.getLastColumn())
      .getValues()[0]; // 현재 행의 모든 값 가져오기

    // H 열 값 가져오기
    var hColumnValue = currentRowValues[7]; // H 열은 인덱스 7 (0부터 시작)
    // F 열 값 가져오기
    var fColumnValue = currentRowValues[5]; // F 열은 인덱스 5

    // H 열이 "prompter"이고 F 열에 "답변"이라는 단어가 독립적으로 존재하는 경우에만 처리
    if (hColumnValue === "prompter" && typeof fColumnValue === "string") {
      var fColumnWords = fColumnValue.split(/\s+/); // 공백으로 단어 분리
      var indexOfAnswer = fColumnWords.indexOf(separation_word); // "답변"

      if (indexOfAnswer !== -1) {
        // "답변" 단어를 포함하여 이후의 텍스트 추출
        var responseText = fColumnWords.slice(indexOfAnswer).join(" "); // "답변" 포함 이후의 모든 문자를 조합
        var responseTextToMove = responseText.trim(); // 공백 제거

        // 추출한 문자들을 다음 행의 F 열에 삽입
        sheet.getRange(row + 1, 6).setValue(responseTextToMove);

        // 현재 행의 F 열에서 "답변" 이후의 문자 제거, "답변"까지만 남기기
        var updatedFColumnValue = fColumnWords
          .slice(0, indexOfAnswer)
          .join(" ")
          .trim(); // "답변"까지 포함
        sheet.getRange(row, 6).setValue(updatedFColumnValue);
      }
    }
  }
}
