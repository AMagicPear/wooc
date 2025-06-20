const getBackgroundColor = (username: string) => {
    let hash = 5381; // djb2初始值
    for (let i = 0; i < username.length; i++) {
        // 哈希算法：hash * 33 + 字符编码
        hash = (hash << 5) + hash + username.charCodeAt(i);
    }
    const hue = Math.abs(hash % 360);
    return `hsl(${hue}, 70%, 80%)`;
};

export default getBackgroundColor;