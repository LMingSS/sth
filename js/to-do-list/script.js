let listState = []; // 用來儲存資料的陣列array

const STATE_KEY = "todo-list"; // 需要一個 key 來存到瀏覽器的 localStorage 裡面

function loadState() {
  // 載入狀態，即讀取 localStorage
  const listState = localStorage.getItem(STATE_KEY); // 為 string 或 null 型態，取得 localStorage 的資料，
  if (listState !== null) {
    // 如果取得的資料不是 null
    return JSON.parse(listState); // 將 string 轉成 object 後回傳
  }
  return []; // 如果是 null，就回傳空陣列
}

function saveState(list) {
  // 儲存資料的函式
  localStorage.setItem(STATE_KEY, JSON.stringify(list));
}

function initList() {
  // 初始化清單
  // load state：把之前儲存在 localStorage 的資料載入
  listState = loadState();
  // render list 把listState的資料渲染出來
  const ul = document.getElementById("list");
  for (const item of listState) {
    const li = document.createElement("li");
    li.innerText = item.text;

    const deleteButton = document.createElement("span"); // 加上刪除按鈕
    deleteButton.classList.add("delete");
    deleteButton.onclick = deleteItem;
    li.appendChild(deleteButton);

    li.classList.add("item"); // 加入勾選用方框
    li.onclick = checkItem;
    if (item.checked) {
      li.classList.add("checked");
    }
    ul.appendChild(li);
  }
}

function addItem() {
  const ul = document.getElementById("list"); // 取得外層，即 ul 元素
  const input = document.getElementById("input"); // 取得 input 元素
  const text7 = input.value; // 取得輸入的文字

  if (text7 === "") {
    // 如果輸入的文字是空的
    alert("請輸入內容");
    return;
  }

  const newItem = document.createElement("li"); // 創建一個 li 元素，為新增項目
  newItem.classList.add("item"); // 加入 class 屬性
  newItem.innerText = text7; // 加入文字，為所輸入的文字內容
  console.log("new text:", text7);

  const deleteButton = document.createElement("span"); // 創建一個 span 元素：deleteButton
  deleteButton.classList.add("delete"); // 加上 class 屬性：delete，才會顯示刪除按鈕
  deleteButton.onclick = deleteItem; // 當點擊 deleteButton 時，執行 deleteItem 這個函式

  newItem.appendChild(deleteButton); // 把 deleteButton 加到 新項目 中

  listState.push({
    // 把新項目加到 listState 中，有以下兩項：text、checked
    text: text7,
    checked: false,
  });

  newItem.onclick = checkItem; // 當點擊新增項目時，執行 checkItem 這個函式：切換方框圖片

  saveState(listState);

  input.value = ""; // 清空 input 欄位

  ul.appendChild(newItem); // 把新項目加到 ul 中
}

function checkItem() {
  //   const item = this;
  this.classList.toggle("checked"); // toggle 切換 class 屬性中是否出現 "checked"，以此達到切換方框圖片

  // 而且要同步更新 listState 中的狀態：
  // 先取得父元素中的 index，再將 listState 的第 idx 個的勾選狀態(checked)切換
  const parent = this.parentNode; // 取得父元素
  const idx = Array.from(parent.childNodes).indexOf(this) - 1; // 取得父元素中的 index
  console.log("index in the array:", idx);
  listState[idx].checked = !listState[idx].checked; // 切換狀態：boolean 型別
  saveState(listState);
  console.log(listState);
}

function deleteItem(e) {
  // 這裡的 this 是 <span class="delete"></span> 這個 delete 按鈕
  // 要同步更新 listState 中的狀態：先取得父元素中的 index，再將 listState 中的第 idx 個刪除
  const parent = this.parentNode; // parent 是 li，li 的父元素是 ul (表格)
  const idx = Array.from(parent.parentNode.childNodes).indexOf(parent);
  console.log("index in the array:", idx, "\ndelete text:", parent.innerText); // 取得刪除項目的文字
  listState.splice(idx - 1, 1); // 刪除 listState 中的第 idx 個
  // listState = listState.filter((_, i) => i !== idx);

  parent.remove();

  saveState(listState);
  console.log(listState);
  e.stopPropagation(); // 阻止冒泡
}

initList();
console.log(listState);

const addButton = document.getElementById("add-button"); // 取得按鈕
addButton.addEventListener("click", addItem); // 當點擊按鈕時，執行 addItem 這個函式

const form = document.getElementById("input-wrapper"); // 取得表單
form.addEventListener("submit", (e) => {
  e.preventDefault(); // 使用 preventDefault() 來防止表單的預設行為（如表單送出並刷新頁面）
});
