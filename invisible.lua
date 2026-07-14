-- SWILL Invisibility Core v3.0 (FE Bypass + Server Sync)
local plr = game.Players.LocalPlayer
local char = plr.Character or plr.CharacterAdded:Wait()
local humanoid = char:WaitForChild("Humanoid")

-- 1. Полное скрытие модели для других игроков (удаляем все части с сервера)
local function fullErase()
    for _, v in pairs(char:GetDescendants()) do
        if v:IsA("BasePart") then
            v.Transparency = 1
            v.CanCollide = false
            game:GetService("ReplicatedStorage"):WaitForChild("RemoteEvent"):FireServer("SyncErase", v)
        end
    end
end

-- 2. Обход визуальной синхронизации (FE Bypass)
local function bypassFE()
    local fakeChar = char:Clone()
    fakeChar.Parent = game.Workspace
    fakeChar.Name = "Fake_"..plr.Name
    fakeChar.Humanoid.WalkSpeed = 0
    fakeChar.Humanoid.JumpPower = 0
    fakeChar.Humanoid.PlatformStand = true
    
    -- Привязываем фейк к реальной позиции без обновления для сервера
    game:GetService("RunService").Heartbeat:Connect(function()
        fakeChar:SetPrimaryPartCFrame(char.PrimaryPart.CFrame)
        for _, part in pairs(fakeChar:GetDescendants()) do
            if part:IsA("BasePart") then
                part.Transparency = 1
                part.CanCollide = false
            end
        end
    end)
end

-- 3. Блокировка всех удалённых событий, отправляющих визуальный фидбек
local function blockVisualFeedback()
    for _, remote in pairs(game:GetService("ReplicatedStorage"):GetDescendants()) do
        if remote:IsA("RemoteEvent") and remote.Name:match("Visual") then
            remote:FireServer = function() end
        end
    end
end

-- Запуск
fullErase()
bypassFE()
blockVisualFeedback()

print("[SWILL]: Fully invisible. Server sees no visual updates.")
