

        let lastExpenseConfig=null
        async function loadReportData(config){
            lastExpenseConfig=config
            try {
                const result=await request(config.url,"post",config.body)
    
                if (result.success) {
                    const expenseData=result.data.expense;
                    const incomeData=result.data.income;
                    const remainingData=result.data.remaining;

                    document.getElementById(config.expenseId).innerText=`RMB ${expenseData}`;
                    document.getElementById(config.incomeId).innerText=`RMB ${incomeData}`;
                    document.getElementById(config.remainingId).innerText=`RMB ${remainingData}`;   
                } else {
                    console.error("接口返回失败",result.message);
                }
            } catch (error){
                console.error("加载失败",error)
            }
        }


        async function loadExpenseData(config) {
            try {
                const top_n=10;
                const result=await request(config.url,"post",config.body)
    
                if(result.success){
                    renderExpenseTable(result.data,"expenseList")
                }
            } catch (error){
                console.error("加载失败",error )
            }
                
        }


        
        async function deleteExpense(ts_id) {
            if(!confirm("确定要删除吗？")) return;

            try{
                const res=await fetch(`/delete_ts/${ts_id}`,{
                    method:"delete"
                })

                const result=await res.json()
                if(result.success){
                    loadExpenseData(lastExpenseConfig);
                } else{
                    alert("删除失败");
                }
            } catch (error){
                console.error("删除失败",error)
            }
                
        }

        async function editExpense(ts_id) {
            window.location.href=`/edit-page/${ts_id}`
        }

      