const draggables_1 = document.querySelectorAll('.draggable_1')
const draggables_2 = document.querySelectorAll('.draggable_2')
const column_1s = document.querySelectorAll('.column_1')
const column_2s = document.querySelectorAll('.column_2')

draggables_1.forEach(draggable => {
  draggable.addEventListener('dragstart', _ => {
    draggable.classList.add('dragging_1')
  })

  draggable.addEventListener('dragend', _ => {
    draggable.classList.remove('dragging_1')
  })

})

column_1s.forEach(column_1 => {
  column_1.addEventListener('dragover', e => {
    e.preventDefault()
    const afterElement = getDragAfterElement_column_1(column_1, e.clientY)
    const cur_draggable = document.querySelector('.dragging_1')
    if (afterElement == null) {
      console.log(afterElement)
      column_1.appendChild(cur_draggable)
    } else {
      column_1.insertBefore(cur_draggable, afterElement)
    }
  })
})

function getDragAfterElement_column_1(column_1, y) {
  const draggableElemnts = [...column_1.querySelectorAll('.draggable_1:not(.dragging_1)')]

  return draggableElemnts.reduce((closest, child) => {
    const box = child.getBoundingClientRect()
    const offset = y - box.top - box.height / 2
    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child }
    } else {
      return closest
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element
}

draggables_2.forEach(draggable => {
  draggable.addEventListener('dragstart', _ => {
    draggable.classList.add('dragging_2')
  })

  draggable.addEventListener('dragend', _ => {
    draggable.classList.remove('dragging_2')
  })

})

column_2s.forEach(column_2 => {
  column_2.addEventListener('dragover', e => {
    e.preventDefault()
    const afterElement = getDragAfterElement_column_2(column_2, e.clientY)
    const cur_draggable = document.querySelector('.dragging_2')
    if (afterElement == null) {
      column_2.appendChild(cur_draggable)
    } else {
      column_2.insertBefore(cur_draggable, afterElement)
    }
  })
})

function getDragAfterElement_column_2(column_2, y) {
  const draggableElemnts = [...column_2.querySelectorAll('.draggable_2:not(.dragging_2)')]

  return draggableElemnts.reduce((closest, child) => {
    const box = child.getBoundingClientRect()
    const offset = y - box.top - box.height / 2
    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child }
    } else {
      return closest
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element
}

$('#save-link').click(function () {
  var retContent = [];
  var retString = '';
  $('tbody tr').each(function (idx, elem) {
    var elemText = '';
    var i = 0
    $(elem).children('td').each(function (childIdx, childElem) {
      if (i == 0) {
        text = ''
        $(childElem).find('.txt').each(function(Idx, childText){
          text += $(childText).val() + '\n'
        });
        elemText += '(en)' + text;
        i = 1;
      } else if (i == 1){
        if (!$(childElem).find('.box_check').is(":checked")){
          elemText = '+' + elemText
        }
        i = 2
      } else if (i == 2){
        text = ''
        $(childElem).find('.txt').each(function(Idx, childText){
          text += $(childText).val() + '\n'
        });
        elemText += '(vi)' + text;
        i = 0
      }
    });
    retContent.push(`${elemText}`);
  });
  retString = retContent.join("\n\n")
  var file = new Blob([retString], { type: 'text/plain' });
  var btn = $('#save-link');
  btn.attr("href", URL.createObjectURL(file));
  btn.prop("download", "data.txt");
})

$(document).ready(function() {
  $('textarea').on('keyup keydown', function() {
    $(this).height(0);
    $(this).height(this.scrollHeight);
  });
});



// $.fn.enterKey = function (fnc) {
//   return this.each(function () {
//       $(this).keypress(function (ev) {
//           var keycode = (ev.keyCode ? ev.keyCode : ev.which);
//           if (keycode == '13') {
//               fnc.call(this);
//           }
//       })
//   })
// }

// $('.txt').enterKey(e => {
//       var pos= $(e).prop('selectionStart');
//       var s=$(e).html()
//       console.log(pos,s)
// });



// $.fn.getCursorPosition = function () {
//   var el = $(this).get(0);
//   var pos = 0;
//   if ('selectionStart' in el) {
//     pos = el.selectionStart;
//   } else if ('selection' in document) {
//     el.focus();
//     var Sel = document.selection.createRange();
//     var SelLength = document.selection.createRange().text.length;
//     Sel.moveStart('character', -el.value.length);
//     pos = Sel.text.length - SelLength;
//   }
//   return pos;
// }