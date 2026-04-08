// ---------- Node structure ----------
class Node {
  constructor(data) {
    this.data = data;
    this.next = null;
  }
}

// ---------- Linked List class ----------
class LinkedList {
  constructor() {
    this.head = null;
  }

  // add node at end
  append(data) {
    let newNode = new Node(data);

    if (this.head === null) {
      this.head = newNode;
      return;
    }

    let curr = this.head;
    while (curr.next !== null) {
      curr = curr.next;
    }
    curr.next = newNode;
  }

  // print list
  print() {
    let curr = this.head;
    let result = "";

    while (curr !== null) {
      result += curr.data + " → ";
      curr = curr.next;
    }
    console.log(result + "null");
  }
}

// ---------- Reverse a linked list ----------
function reverse(head) {
  let prev = null;
  let curr = head;

  while (curr !== null) {
    let nextNode = curr.next;
    curr.next = prev;
    prev = curr;
    curr = nextNode;
  }
  return prev;
}

// ---------- Add two linked lists ----------
function addTwoLists(l1, l2) {
  let dummy = new Node(0);
  let curr = dummy;
  let carry = 0;

  while (l1 !== null || l2 !== null || carry !== 0) {
    let sum = carry;

    if (l1 !== null) {
      sum += l1.data;
      l1 = l1.next;
    }

    if (l2 !== null) {
      sum += l2.data;
      l2 = l2.next;
    }

    carry = Math.floor(sum / 10);
    curr.next = new Node(sum % 10);
    curr = curr.next;
  }

  return dummy.next;
}

// ---------- CREATE LIST 1 ----------
let list1 = new LinkedList();
list1.append(3);
list1.append(4);
list1.append(2);

// ---------- CREATE LIST 2 ----------
let list2 = new LinkedList();
list2.append(4);
list2.append(5);
list2.append(6);

// ---------- PRINT ORIGINAL ----------
console.log("List 1:");
list1.print();

console.log("List 2:");
list2.print();

// ---------- REVERSE BOTH ----------
let rev1 = reverse(list1.head);
let rev2 = reverse(list2.head);

// ---------- ADD ----------
let sumList = addTwoLists(rev1, rev2);

// ---------- REVERSE RESULT ----------
let finalResult = reverse(sumList);

// ---------- PRINT FINAL RESULT ----------
console.log("Final Result:");
let temp = finalResult;
let output = "";
while (temp !== null) {
  output += temp.data + " → ";
  temp = temp.next;
}
console.log(output + "null");
