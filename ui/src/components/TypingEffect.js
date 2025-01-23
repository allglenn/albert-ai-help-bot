import React, { useState, useEffect } from 'react';
import { Typography } from '@mui/material';

const TypingEffect = ({ text = '', speed = 20 }) => {
    const [displayedText, setDisplayedText] = useState('');
    const [currentIndex, setCurrentIndex] = useState(0);

    // Reset effect when text changes
    useEffect(() => {
        setDisplayedText('');
        setCurrentIndex(0);
    }, [text]);

    // Handle typing animation
    useEffect(() => {
        // Safety check
        if (!text) return;

        // If we haven't finished typing
        if (currentIndex < text.length) {
            const timer = setTimeout(() => {
                // Add more characters at once for longer texts
                const charsToAdd = text.length > 100 ? 3 : 1;
                const nextIndex = Math.min(currentIndex + charsToAdd, text.length);
                setDisplayedText(text.substring(0, nextIndex));
                setCurrentIndex(nextIndex);
            }, speed);

            return () => clearTimeout(timer);
        }
    }, [text, currentIndex, speed]);

    return (
        <Typography component="div" style={{ whiteSpace: 'pre-wrap' }}>
            {displayedText}
        </Typography>
    );
};

export default TypingEffect;