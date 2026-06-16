
        async function renderExpenseTable(expense,tbodyId) {
            if(!expense || expense.length == 0) {
                const tbody=document.getElementById(tbodyId);
                const tr=document.createElement("tr")
                const td=document.createElement("td")
                td.textContent = "暂无数据"
                tr.appendChild(td)
                tbody.appendChild(tr)
                return;
            }

            for (const item of expense) {
                const tbody=document.getElementById(tbodyId);
                const tr=document.createElement("tr")

                const td1=document.createElement("td")
                td1.textContent = item.category_name

                const td2=document.createElement("td")
                td2.textContent = item.amount.toFixed(2)

                const td3=document.createElement("td")
                td3.textContent = item.note

                const td4=document.createElement("td")
                td4.textContent=item.date

                const td5=document.createElement("td")
                const btn1=document.createElement("button")
                btn1.textContent="编辑"
                btn1.addEventListener("click",() => {
                    editExpense(item.transaction_id)
                })

                td5.appendChild(btn1)

                const td6=document.createElement("td")
                const btn2=document.createElement("button")
                btn2.textContent="删除"
                btn2.addEventListener("click", () => {
                    deleteExpense(item.transaction_id)
                })
                td6.appendChild(btn2)

                tr.appendChild(td1)
                tr.appendChild(td2)
                tr.appendChild(td3)
                tr.appendChild(td4)
                tr.appendChild(td5)
                tr.appendChild(td6)

                tbody.appendChild(tr)
            }

        }

