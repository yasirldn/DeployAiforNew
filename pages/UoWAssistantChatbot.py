import streamlit as st
import streamlit.components.v1 as components

# UoW Assistant Chatbot
watson_script = """
<script>
    window.watsonAssistantChatOptions = {
        integrationID: "b7b7c8ae-f11e-4bdd-a1b3-6bee7697de11",
        region: "eu-gb",
        serviceInstanceID: "1be8a1d9-b9c1-4017-ad84-d1858b6d1605",
        onLoad: async (instance) => { await instance.render(); }
    };
    setTimeout(function(){
        const t=document.createElement('script');
        t.src="https://web-chat.global.assistant.watson.appdomain.cloud/versions/" + (window.watsonAssistantChatOptions.clientVersion || 'latest') + "/WatsonAssistantChatEntry.js";
        document.head.appendChild(t);
    });
</script>
"""

# Embed the chatbot script using Streamlit components
components.html(watson_script, height=700)
