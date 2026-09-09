package com.vkrief.spotthecar;

import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

// Le SDK Google UMP ecrit les signaux TCF (IAB Transparency & Consent Framework)
// dans les SharedPreferences par defaut de l'app une fois le formulaire de
// consentement resolu. Le plugin @capacitor-community/admob n'expose pas ces
// details cote JS (juste un statut global "canRequestAds") -- ce plugin les lit
// directement pour permettre de forcer une requete non personnalisee (npa)
// quand l'utilisateur a explicitement refuse le tracking, sans degrader les
// pubs de ceux qui ont accepte.
@CapacitorPlugin(name = "Tcf")
public class TcfPlugin extends Plugin {

    // ID vendeur IAB de Google sous TCF v2.2 (liste officielle Global Vendor List).
    private static final int GOOGLE_TCF_VENDOR_ID = 755;

    @PluginMethod
    public void getConsentSignals(PluginCall call) {
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(getContext());

        int gdprApplies = prefs.getInt("IABTCF_gdprApplies", -1);
        String purposeConsents = prefs.getString("IABTCF_PurposeConsents", "");
        String vendorConsents = prefs.getString("IABTCF_VendorConsents", "");

        boolean gdprApplied = gdprApplies == 1;
        boolean purpose1Granted = purposeConsents.length() >= 1 && purposeConsents.charAt(0) == '1';
        boolean googleVendorGranted = vendorConsents.length() >= GOOGLE_TCF_VENDOR_ID
            && vendorConsents.charAt(GOOGLE_TCF_VENDOR_ID - 1) == '1';

        // Hors zone GDPR (pas de TC string), ou consentement complet accorde a Google :
        // rien a restreindre. Sinon (refus, partiel, ou etat indetermine en zone GDPR) :
        // on demande des pubs non personnalisees par securite.
        boolean fullConsentGranted = !gdprApplied || (purpose1Granted && googleVendorGranted);

        JSObject ret = new JSObject();
        ret.put("gdprApplies", gdprApplied);
        ret.put("fullConsentGranted", fullConsentGranted);
        call.resolve(ret);
    }
}
