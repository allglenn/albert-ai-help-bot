import React, { useState } from "react";
import ChatModal from "./ChatModal";

const [chatOpen, setChatOpen] = useState(false);
const [selectedAssistantId, setSelectedAssistantId] = useState<number | null>(
  null
);

// When opening chat
const handleOpenChat = (assistantId: number) => {
  setSelectedAssistantId(assistantId);
  setChatOpen(true);
};

// In your JSX
{
  selectedAssistantId && (
    <ChatModal
      open={chatOpen}
      onClose={() => setChatOpen(false)}
      assistantId={selectedAssistantId}
    />
  );
}
