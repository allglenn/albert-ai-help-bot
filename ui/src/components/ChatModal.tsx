import React, { useState, useRef, useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  IconButton,
  Box,
  TextField,
  Button,
  Typography,
  Avatar,
  CircularProgress,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import SendIcon from "@mui/icons-material/Send";
import { useAuth } from "../contexts/AuthContext";
import { apiClient } from "../utils/apiClient";
import TypingEffect from "./TypingEffect";

interface Message {
  content: string;
  emitter: "USER" | "ASSISTANT";
  created_at: string;
}

interface ChatModalProps {
  open: boolean;
  onClose: () => void;
  assistantId: number;
}

const ChatModal: React.FC<ChatModalProps> = ({
  open,
  onClose,
  assistantId,
}) => {
  const { token } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState("");
  const [chatId, setChatId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [assistant, setAssistant] = useState<any>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize chat when modal opens
  useEffect(() => {
    if (open && !chatId) {
      initializeChat();
    }
  }, [open]);

  const initializeChat = async () => {
    try {
      setLoading(true);
      const response = await apiClient.post(
        `/help-assistant/${assistantId}/chat/init`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      console.log("Chat initialized with ID:", response.data.chat_id); // Debug log
      setChatId(response.data.chat_id);
      setAssistant(response.data.assistant);
      setMessages(response.data.messages);
    } catch (error) {
      console.error("Error initializing chat:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!newMessage.trim() || !chatId) return;

    try {
      // Store message before clearing input
      const messageContent = newMessage;

      // Immediately add user message and clear input
      const userMessage: Message = {
        content: messageContent,
        emitter: "USER",
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, userMessage]);
      setNewMessage("");

      // Show loading state but don't block the UI
      setLoading(true);

      console.log("Sending message to chat:", chatId); // Debug log

      // Send message to API with correct endpoint and chat ID
      const response = await apiClient.post(
        `/help-assistant/${assistantId}/chat/${chatId}/message`, // Include chatId in URL
        {
          content: messageContent,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      // Add assistant response
      if (response.data.message) {
        const assistantMessage: Message = {
          content: response.data.message.content,
          emitter: "ASSISTANT",
          created_at: response.data.message.created_at,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (error) {
      console.error("Error sending message:", error);
      console.error("ChatId:", chatId); // Debug log
      // Optionally show error to user
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box display="flex" alignItems="center" gap={2}>
            {assistant?.operator_pic && (
              <Avatar
                src={assistant.operator_pic}
                alt={assistant?.operator_name}
                sx={{ width: 40, height: 40 }}
              />
            )}
            <Typography variant="h6">{assistant?.operator_name}</Typography>
          </Box>
          <IconButton onClick={onClose}>
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>
      <DialogContent>
        <Box
          sx={{
            height: "60vh",
            display: "flex",
            flexDirection: "column",
          }}
        >
          {/* Messages Area */}
          <Box
            sx={{
              flexGrow: 1,
              overflowY: "auto",
              mb: 2,
              p: 2,
            }}
          >
            {messages.map((message, index) => (
              <Box
                key={index}
                sx={{
                  display: "flex",
                  justifyContent:
                    message.emitter === "USER" ? "flex-end" : "flex-start",
                  mb: 2,
                }}
              >
                <Box
                  sx={{
                    maxWidth: "70%",
                    backgroundColor:
                      message.emitter === "USER" ? "primary.main" : "grey.100",
                    color:
                      message.emitter === "USER" ? "white" : "text.primary",
                    borderRadius: 2,
                    p: 2,
                  }}
                >
                  {message.emitter === "ASSISTANT" ? (
                    <TypingEffect text={message.content} />
                  ) : (
                    <Typography>{message.content}</Typography>
                  )}
                </Box>
              </Box>
            ))}
            <div ref={messagesEndRef} />
          </Box>

          {/* Input Area */}
          <Box
            sx={{
              display: "flex",
              gap: 1,
              p: 2,
              borderTop: 1,
              borderColor: "divider",
            }}
          >
            <TextField
              fullWidth
              multiline
              maxRows={4}
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Tapez votre message..."
              disabled={loading}
              sx={{ backgroundColor: "background.paper" }}
            />
            <Button
              variant="contained"
              onClick={handleSendMessage}
              disabled={!newMessage.trim() || loading}
              endIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
            >
              Envoyer
            </Button>
          </Box>
        </Box>
      </DialogContent>
    </Dialog>
  );
};

export default ChatModal;
