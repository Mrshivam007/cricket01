if team1_current_run_rate is None:
                                team1_run_rate = ""
                            elif team1_current_run_rate >= 8:
                                team1_run_rate = 8
                            elif team1_current_run_rate <= 6:
                                team1_run_rate = 6
                            else:
                                team1_run_rate = team1_current_run_rate
                                
                            if team2_current_run_rate is None:
                                team2_run_rate = ""
                            if team2_current_run_rate >= 8:
                                team2_run_rate = 8
                            elif team2_current_run_rate <= 6:
                                team2_run_rate = 6
                            else:
                                team2_run_rate = team2_current_run_rate

                            if team1_wicket >= 1 and team1_wicket <= 5:
                                team1_run_rate = (team1_current_run_rate + 2) - (team1_wicket * 0.5)
                            elif team1_wicket >= 6:
                                team1_run_rate = team1_current_run_rate
                            else:
                                team1_run_rate = team1_run_rate      

                            if team2_wicket >= 1 and team2_wicket <= 5:
                                team2_run_rate = (team2_current_run_rate + 2) - (team2_wicket * 0.5)
                            elif team2_wicket >= 6:
                                team2_run_rate = team2_current_run_rate
                            else:
                                team2_run_rate = team2_run_rate