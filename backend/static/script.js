const button = document.getElementById("generateBtn");
const output = document.getElementById("output");
const loading = document.getElementById("loading");
button.addEventListener("click", async () => {

    const email = document.getElementById("emailInput").value;
    const tone = document.getElementById("tone").value;
    const length = document.getElementById("length").value;

    output.textContent = "";

    button.disabled = true;
    button.innerText = "Generating...";

    try {
        loading.style.display = "block";
        const response = await fetch("/generate", {
            
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email,
                tone,
                length
            })

        });

       output.textContent = "";

const reader = response.body.getReader();

const decoder = new TextDecoder();

while (true) {

    const { done, value } = await reader.read();

    if (done) break;

    output.textContent += decoder.decode(value);

}

       loading.style.display = "none";
    } catch (error) {
        loading.style.display = "none";
        output.textContent = "Error connecting to backend.";

    }

    button.disabled = false;
    button.innerText = "Generate Reply";
    
});
const copyBtn = document.getElementById("copyBtn");

copyBtn.addEventListener("click", () => {

    const reply = output.textContent;

    if (reply.trim() === "") {
        alert("No reply to copy!");
        return;
    }

    navigator.clipboard.writeText(reply);

    copyBtn.innerText = "✅ Copied!";

    setTimeout(() => {
        copyBtn.innerText = "📋 Copy Reply";
    }, 2000);

});
document.getElementById("clearBtn").addEventListener("click",()=>{

document.getElementById("emailInput").value="";

output.textContent="";

});