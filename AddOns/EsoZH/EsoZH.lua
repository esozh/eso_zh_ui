local EsoZH = {}
EsoZH.name = "EsoZH"
EsoZH.Flags = { "en", "zh" }

function EsoZH_Change(lang)
    zo_callLater(function()
        SetCVar("language.2", lang)
        ReloadUI()
    end, 500)
end

function EsoZH:RefreshUI()
    local flagControl
    local count = 0
    local flagTexture
    for _, flagCode in pairs(EsoZH.Flags) do
        flagTexture = "EsoZH/flags/"..flagCode..".dds"
        flagControl = GetControl("EsoZH_FlagControl_"..tostring(flagCode))
        if flagControl == nil then
            flagControl = CreateControlFromVirtual("EsoZH_FlagControl_", EsoZHUI, "EsoZH_FlagControl", tostring(flagCode))
            GetControl("EsoZH_FlagControl_"..flagCode.."Texture"):SetTexture(flagTexture)
            if EsoZH:GetLanguage() ~= flagCode then
                flagControl:SetAlpha(0.3)
                if flagControl:GetHandler("OnMouseDown") == nil then flagControl:SetHandler("OnMouseDown", function() EsoZH_Change(flagCode) end) end
            end
        end
        flagControl:ClearAnchors()
        flagControl:SetAnchor(LEFT, EsoZHUI, LEFT, 14 +count*34, 0)
        count = count + 1
    end
    EsoZHUI:SetDimensions(25 +count*34, 50)
    EsoZHUI:SetMouseEnabled(true)
end

function EsoZH:GetLanguage()
    local lang = GetCVar("language.2")
    
    if(lang == "zh") then return lang end
    return "en"
end

function EsoZH:OnInit(eventCode, addOnName)
    if (addOnName):find("^ZO_") then return end

    for _, flagCode in pairs(EsoZH.Flags) do
        ZO_CreateStringId("SI_BINDING_NAME_"..string.upper(flagCode), string.upper(flagCode))
    end

    SetSCTKeyboardFont("EsoZH/fonts/univers67.otf|29|soft-shadow-thick")
    SetNameplateKeyboardFont("EsoZH/fonts/univers67.otf", 4)
    SetNameplateGamepadFont("EsoZH/fonts/ftn87.otf", 4)

    if LibStub then
        local LMP = LibStub("LibMediaProvider-1.0", true)
        if LMP then
            LMP.MediaTable.font["Univers 67"] = nil
            LMP.MediaTable.font["Univers 57"] = nil
            LMP.MediaTable.font["Skyrim Handwritten"] = nil
            LMP.MediaTable.font["ProseAntique"] = nil
            LMP.MediaTable.font["Trajan Pro"] = nil
            LMP.MediaTable.font["Futura Condensed"] = nil
            LMP.MediaTable.font["Futura Condensed Bold"] = nil
            LMP.MediaTable.font["Futura Condensed Light"] = nil
            LMP:Register("font", "Univers 67", "EsoZH/fonts/univers67.otf")
            LMP:Register("font", "Univers 57", "EsoZH/fonts/univers57.otf")
            LMP:Register("font", "Skyrim Handwritten", "EsoZH/fonts/handwritten_bold.otf")
            LMP:Register("font", "ProseAntique", "EsoZH/fonts/proseantiquepsmt.otf")
            LMP:Register("font", "Trajan Pro", "EsoZH/fonts/trajanpro-regular.otf")
            LMP:Register("font", "Futura Condensed", "EsoZH/fonts/ftn57.otf")
            LMP:Register("font", "Futura Condensed Bold", "EsoZH/fonts/ftn87.otf")
            LMP:Register("font", "Futura Condensed Light", "EsoZH/fonts/ftn47.otf")
            LMP:SetDefault("font", "Univers 57")
        end
    end

    EsoZH:RefreshUI()

    function ZO_GameMenu_OnShow(control)
        if control.OnShow then
            control.OnShow(control.gameMenu)
            EsoZHUI:SetHidden(hidden)
        end
    end
    
    function ZO_GameMenu_OnHide(control)
        if control.OnHide then
            control.OnHide(control.gameMenu)
            EsoZHUI:SetHidden(not hidden)
        end
    end
end

EVENT_MANAGER:RegisterForEvent("EsoZH_OnAddOnLoaded", EVENT_ADD_ON_LOADED, function(_event, _name) EsoZH:OnInit(_event, _name) end)
