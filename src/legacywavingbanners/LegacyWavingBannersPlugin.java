package legacywavingbanners;

import com.fs.starfarer.api.BaseModPlugin;
import com.fs.starfarer.api.Global;
import com.fs.starfarer.api.campaign.FactionAPI;
import lunalib.lunaSettings.LunaSettings;
import lunalib.lunaSettings.LunaSettingsListener;

public class LegacyWavingBannersPlugin extends BaseModPlugin {

    // 1. Register the listener when the application starts
    @Override
    public void onApplicationLoad() {
        // Check if LunaLib is enabled to prevent crashes (soft dependency) [2, 3]
        if (Global.getSettings().getModManager().isModEnabled("lunalib")) {
            LunaSettings.addSettingsListener(new MySettingsListener()); [4]
        }
    }

    // 2. Apply the flag when a save game is loaded [3]
    @Override
    public void onGameLoad(boolean newGame) {
        applyHegemonyFlag();
    }

    // 3. Logic to refresh the flag based on the current LunaLib selection
    public static void applyHegemonyFlag() {
        // Ensure we are in the campaign state before trying to access the sector [4]
        if (Global.getSector() == null) return;

        FactionAPI faction = Global.getSector().getFaction("hegemony");
        String choice = "default";

        if (Global.getSettings().getModManager().isModEnabled("lunalib")) {
            // Retrieve the user's choice from the CSV fieldID [5, 6]
            choice = LunaSettings.getString("legacywavingbanners", "hegemonyFlag");
        }

        // Set the flag based on user choice [6]
        if ("alt".equals(choice)) {
            faction.setCustomFlag("graphics/factions/hegemony_alt.png");
        } else {
            faction.setCustomFlag("graphics/factions/hegemony.png");
        }
    }

    // 4. The Listener class that waits for setting changes
    public static class MySettingsListener implements LunaSettingsListener {
        @Override
        public void settingsChanged(String modID) {
            // Only trigger if the changes were made to THIS mod [7]
            if ("legacywavingbanners".equals(modID)) {
                applyHegemonyFlag();
            }
        }
    }
}