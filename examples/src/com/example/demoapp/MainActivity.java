/*
 * Демонстрационный (фейковый) исходник для SDK-Sanitizer.
 * Намеренно импортирует несколько трекерных SDK и упоминает их эндпоинты,
 * чтобы скан показал срабатывания по code- и network-сигнатурам.
 * Это НЕ рабочее приложение и не должно компилироваться/запускаться.
 */
package com.example.demoapp;

import android.app.Activity;
import android.os.Bundle;

// Трекерные SDK (code-сигнатуры)
import com.google.android.gms.ads.MobileAds;
import com.google.android.gms.ads.AdView;
import com.google.firebase.analytics.FirebaseAnalytics;
import com.google.firebase.crashlytics.FirebaseCrashlytics;
import com.facebook.FacebookSdk;
import com.appsflyer.AppsFlyerLib;
import com.amplitude.api.Amplitude;
import io.branch.referral.Branch;
import com.segment.analytics.Analytics;
import io.sentry.Sentry;
import com.unity3d.ads.UnityAds;
import com.applovin.sdk.AppLovinSdk;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Инициализация рекламных и аналитических SDK
        MobileAds.initialize(this);
        AdView adView = new AdView(this);

        FirebaseAnalytics analytics = FirebaseAnalytics.getInstance(this);
        FirebaseCrashlytics.getInstance().setCrashlyticsCollectionEnabled(true);

        FacebookSdk.sdkInitialize(getApplicationContext());
        AppsFlyerLib.getInstance().init("DEV_KEY", null, this);
        Amplitude.getInstance().initialize(this, "AMP_KEY");
        Branch.getAutoInstance(this);
        Sentry.init();
        UnityAds.initialize(this, "GAME_ID", false);
        AppLovinSdk.initializeSdk(this);

        // Эндпоинты (network-сигнатуры) — упомянуты для демонстрации детекта
        String[] endpoints = new String[] {
            "https://app-measurement.com/a",
            "https://graph.facebook.com/v12.0/me",
            "https://api.segment.io/v1/track",
            "https://api.branch.io/v1/open",
            "https://sentry.io/api/store/",
            "https://googleads.g.doubleclick.net/mads/gma"
        };
    }
}
